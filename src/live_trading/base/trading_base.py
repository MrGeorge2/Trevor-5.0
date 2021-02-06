from ...globals.config import Config
from ...nn_model.modelnn import ModelNN
from ..order_manager import OrderManager
from ...data_analysis.models.candle_api import CandleApi
import numpy as np
import pandas as pd
from decimal import Decimal
from ...samples.samples import preprocess_df
from datetime import timedelta, datetime
from typing import List


class TradingInterface:
    SIMULATION = Config.SIMULATION

    def __init__(self, symbol):
        self.nn_model = ModelNN()
        self.symbol = symbol
        self.manager = OrderManager(symbol=self.symbol)
        self.delta = 0
        self.trading_time: timedelta = timedelta(minutes=0)

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
    def total_net_profit(self):
        res = self.manager.total_profit - (self.manager.closed_orders * Config.FEE * 2)
        return round(float(res), 2)

    @property
    def net_profit_per_trade(self):
        res = self.total_net_profit / self.manager.closed_orders if self.manager.closed_orders > 0 else 0
        return round(float(res), 2)

    @staticmethod
    def _get_last_candle(timesteps_to_process):
        last_candle: CandleApi = timesteps_to_process[-1]
        last_candle.open_price = Decimal(last_candle.open_price)
        last_candle.high_price = Decimal(last_candle.high_price)
        last_candle.low_price = Decimal(last_candle.low_price)
        last_candle.close_price = Decimal(last_candle.close_price)

        return last_candle

    def _update_trading_time(self, last_candle: CandleApi):
        """
        Pro volání ve smyčce v backtestu/live_tradingu - počítá dobu tradování podle délky svíček
        :param last_candle:
        :return: None
        """
        delta: timedelta = last_candle.close_time - last_candle.open_time
        self.trading_time += timedelta(seconds=round(float(delta.seconds)))

    def _scrape_candles(self, scraper_func, limit=500):
        scraped = scraper_func()

        candles = [CandleApi(
            open_time=datetime.fromtimestamp(int(candle[0])/1000),
            close_time=datetime.fromtimestamp(int(candle[6])/1000),
            open_price=Decimal(candle[1]),
            high_price=Decimal(candle[2]),
            low_price=Decimal(candle[3]),
            close_price=Decimal(candle[4]),
            volume=Decimal(candle[5]))
            for candle in scraped
        ]

        last_candle: CandleApi = self._get_last_candle(candles)

        return candles, last_candle

    def _preprocess_candles(self, scraped_candles):
        self.delta = self._get_delta(scraped_candles)

        scraped_df = pd.DataFrame(candle.prices_as_dict_live() for candle in scraped_candles)
        preprocesed = preprocess_df(scraped_df, shuffle=False)[0][1]
        # [0] - protoze tam jsou sequence
        # [-1] potrebuju posledni sequenci
        return np.array([preprocesed])

    def _predict_result(self, input_sample):
        return self.nn_model.predict(input_sample)

    def _create_order(self, prediction, last_candle: CandleApi):

        if prediction == 1 and not self.manager.is_order_already_opened(last_candle=last_candle, prediction=prediction):
            # tp: Decimal = last_candle.close_price * Decimal((1 + 0.212 / 100))
            tp: Decimal = last_candle.close_price * Decimal((1 + 0.25 / 100))
            # sl: Decimal = last_candle.close_price * Decimal((1 - 0.05 / 100))
            sl: Decimal = last_candle.close_price * Decimal((1 - 0.15 / 100))
            self.manager.open_long(price=last_candle.close_price, take_profit=tp, stop_loss=sl, last_candle=last_candle)
            return True

        elif prediction == 0 and not self.manager.is_order_already_opened(last_candle=last_candle, prediction=prediction):
            # tp: Decimal = last_candle.close_price * Decimal((1 - 0.25 / 100))
            tp: Decimal = last_candle.close_price * Decimal((1 - 0.25 / 100))
            # sl: Decimal = last_candle.close_price * Decimal((1 + 0.05 / 100))
            sl: Decimal = last_candle.close_price * Decimal((1 + 0.15 / 100))
            self.manager.open_short(price=last_candle.close_price, take_profit=tp, stop_loss=sl, last_candle=last_candle)
            return True

        return False

    def _check_orders(self, last_candle, checktime):
        self.manager.check_opened_orders(last_candle, checktime=checktime)

    def _print_profit(self):
        self.manager.print_profit()

    def run(self):
        """
        Tato metoda musí být přepsaná v implementaci
        :return:
        """
        raise NotImplementedError("Calling base class!")