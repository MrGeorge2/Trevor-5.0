from ..globals.config import Config
from ..api_handler.api_handler import ApiHandler
from ..nn_model.modelnn import ModelNN
from ..samples.samples import Samples, preprocess_df
from ..data_analysis.models.candle_api import CandleApi
import pandas as pd
import numpy as np
import time
from decimal import Decimal
from datetime import datetime, timedelta
from .OrderManager import OrderManager
import logging
from typing import List


class LiveTrading:
    SIMULATION = Config.SIMULATION

    def __init__(self, symbol):
        self.nn_model = ModelNN()
        self.symbol = symbol
        self.manager = OrderManager(symbol=self.symbol)
        self.delta = 0

    @staticmethod
    def __get_delta_for_symbol(candles: List[CandleApi]) -> float:
        if len(candles) <= 0:
            return 0

        first_candle = candles[0]
        last_candle = candles[-1]

        delta = float(last_candle.close_price - first_candle.close_price) / float(last_candle.close_price)
        delta = abs(delta * 100)
        return delta

    def scrape_candles(self):
        api_handler: ApiHandler = ApiHandler.get_new_ApiHandler()
        # scraped = api_handler.get_historical_klines(self.symbol, Config.CANDLE_INTERVAL, "2 hour ago UTC")   # TODO: zkontrolovat casove pasmo
        scraped = api_handler.futures_klines(symbol=self.symbol, interval=Config.CANDLE_INTERVAL, )

        candles = [CandleApi(open_price=candle[1], high_price=candle[2], low_price=candle[3], close_price=candle[4],
                             volume=candle[5]) for candle in scraped]

        last_candle: CandleApi = candles[-1]
        last_candle.open_price = Decimal(last_candle.open_price)
        last_candle.high_price = Decimal(last_candle.high_price)
        last_candle.low_price = Decimal(last_candle.low_price)
        last_candle.close_price = Decimal(last_candle.close_price)

        self.delta = self.__get_delta_for_symbol(candles)
        return candles, last_candle

    @staticmethod
    def preprocess_candles(scraped_candles):
        scraped_df = pd.DataFrame(candle.prices_as_dict_live() for candle in scraped_candles)
        # [0] - protoze tam jsou sequence
        # [-1] potrebuju posledni sequenci

        return np.array([preprocess_df(scraped_df, shuffle=False)[0][-1]])

    def predict_result(self, input_sample):
        return self.nn_model.predict(input_sample)

    def create_order(self, prediction, last_candle: CandleApi):

        if prediction == 1 and not self.manager.is_order_already_opened(last_candle=last_candle, prediction=prediction):
            tp: Decimal = last_candle.close_price * Decimal((1 + 0.2124 / 100))
            sl: Decimal = last_candle.close_price * Decimal((1 - 0.289 / 100))
            self.manager.open_long(price=last_candle.close_price, take_profit=tp, stop_loss=sl)

        elif prediction == 0 and not self.manager.is_order_already_opened(last_candle=last_candle, prediction=prediction):
            tp: Decimal = last_candle.close_price * Decimal((1 - 0.264 / 100))
            sl: Decimal = last_candle.close_price * Decimal((1 + 0.2374 / 100))
            self.manager.open_short(price=last_candle.close_price, take_profit=tp, stop_loss=sl)

    def check_orders(self, last_candle):
        self.manager.check_opened_orders(last_candle)

    def print_profit(self):
        logging.info(f"closed orders: {self.manager.closed_orders}, opened orders: {len(self.manager.opened_orders)} profitable_orders={self.manager.profitable_trades}")
        logging.info(f"total profit: {round(self.manager.total_profit, 4)} %")
        logging.info('')

    def run(self):
        check_new_candle = False

        while True:
            now = datetime.now()
            # if now - time_compare > timedelta(minutes=Config.CANDLE_MINUTES_INTERVAL):
            if 2 < now.second < 5:      # zacatek kazde minuty s rezervou 2s
                check_new_candle = True

            if check_new_candle:
                last_candle: CandleApi
                try:
                    scraped_candles, last_candle = self.scrape_candles()    # scraped candles, last candle in df
                except Exception as e:
                    logging.critical(e)
                    continue

                preprocessed = self.preprocess_candles(scraped_candles=scraped_candles)

                predikce, jistota = self.predict_result(preprocessed)

                logging.info(f"Jistota={jistota} predikce={predikce}")
                if jistota >= 0.70 and self.delta >= Config.MINIMAL_DELTA:
                    self.create_order(prediction=predikce, last_candle=last_candle)

                self.check_orders(last_candle)
                self.print_profit()
                check_new_candle = False
                time.sleep(50)

    @staticmethod
    def trade():
        live_trader = LiveTrading(symbol="BTCUSDT")
        live_trader.run()
