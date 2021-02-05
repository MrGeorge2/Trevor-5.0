from ...globals.config import Config
from ...nn_model.modelnn import ModelNN
from ..order_manager import OrderManager
from ...data_analysis.models.candle_api import CandleApi
from decimal import Decimal
from ...api_handler.api_handler import ApiHandler
import numpy as np
import pandas as pd
import logging
from ...samples.samples import preprocess_df
from datetime import timedelta
from typing import List


class TradingInterface:
    SIMULATION = Config.SIMULATION

    def __init__(self, symbol):
        self.nn_model = ModelNN()
        self.symbol = symbol
        self.manager = OrderManager(symbol=self.symbol)
        self.delta = 0

    @staticmethod
    def _get_delta(candles: List[CandleApi]) -> float:
        if len(candles) <= 0:
            return 0
        last_close = float(candles[-1].close_price)
        first_close = float(candles[0].close_price)

        delta = (first_close - last_close) / last_close
        delta = abs(delta) * 100
        return delta

    @property
    def total_net_profit(self) -> Decimal:
        return self.manager.total_profit - (self.manager.closed_orders * Config.FEE * 2)

    @property
    def net_profit_per_trade(self) -> Decimal:
        return self.total_net_profit / self.manager.closed_orders if self.manager.closed_orders > 0 else 0

    @property
    def trading_time(self) -> timedelta:
        return timedelta(minutes=self.manager.closed_orders)

    @staticmethod
    def _get_last_candle(timesteps_to_process):
        last_candle: CandleApi = timesteps_to_process[-1]
        last_candle.open_price = Decimal(last_candle.open_price)
        last_candle.high_price = Decimal(last_candle.high_price)
        last_candle.low_price = Decimal(last_candle.low_price)
        last_candle.close_price = Decimal(last_candle.close_price)

        return last_candle

    def _scrape_candles(self, scraper_func, limit=500):
        scraped = scraper_func(symbol=self.symbol, interval=Config.CANDLE_INTERVAL, klines=limit)

        candles = [CandleApi(open_price=candle[1], high_price=candle[2], low_price=candle[3], close_price=candle[4],
                             volume=candle[5]) for candle in scraped]

        last_candle: CandleApi = self._get_last_candle(candles)
        self.delta = self._get_delta(candles)

        return candles, last_candle

    @staticmethod
    def _preprocess_candles(scraped_candles):
        scraped_df = pd.DataFrame(candle.prices_as_dict_live() for candle in scraped_candles)
        # [0] - protoze tam jsou sequence
        # [-1] potrebuju posledni sequenci
        return np.array([preprocess_df(scraped_df, shuffle=False)[0]][-1])

    def _predict_result(self, input_sample):
        return self.nn_model.predict(input_sample)

    def _create_order(self, prediction, last_candle: CandleApi):

        if prediction == 1 and not self.manager.is_order_already_opened(last_candle=last_candle, prediction=prediction):
            tp: Decimal = last_candle.close_price * Decimal((1 + 0.2124 / 100))
            sl: Decimal = last_candle.close_price * Decimal((1 - 0.289 / 100))
            self.manager.open_long(price=last_candle.close_price, take_profit=tp, stop_loss=sl)
            return True

        elif prediction == 0 and not self.manager.is_order_already_opened(last_candle=last_candle, prediction=prediction):
            tp: Decimal = last_candle.close_price * Decimal((1 - 0.264 / 100))
            sl: Decimal = last_candle.close_price * Decimal((1 + 0.2374 / 100))
            self.manager.open_short(price=last_candle.close_price, take_profit=tp, stop_loss=sl)
            return True

        return False

    def _check_orders(self, last_candle):
        self.manager.check_opened_orders(last_candle)

    def _print_profit(self):
        self.manager.print_profit()

    def run(self):
        """
        Tato metoda musí být přepsaná v implementaci
        :return:
        """
        raise NotImplementedError("Calling base class!")