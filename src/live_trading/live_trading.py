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


class LiveTrading:
    SIMULATION = Config.SIMULATION

    def __init__(self, symbol):
        self.nn_model = ModelNN()
        self.symbol = symbol
        self.manager = OrderManager(symbol=self.symbol)

    def scrape_candles(self):
        api_handler: ApiHandler = ApiHandler.get_new_ApiHandler()
        scraped = api_handler.get_historical_klines(self.symbol, Config.CANDLE_INTERVAL, "2 hour ago UTC")   # TODO: zkontrolovat casove pasmo
        candles = [CandleApi(open_price=candle[1], high_price=candle[2], low_price=candle[3], close_price=candle[4],
                             volume=candle[5]) for candle in scraped]

        last_candle: CandleApi = candles[-1]
        last_candle.open_price = Decimal(last_candle.open_price)
        last_candle.high_price = Decimal(last_candle.high_price)
        last_candle.low_price = Decimal(last_candle.low_price)
        last_candle.close_price = Decimal(last_candle.close_price)

        return candles, last_candle

    @staticmethod
    def preprocess_candles(scraped_candles):
        scraped_df = pd.DataFrame(candle.prices_as_dict_live() for candle in scraped_candles)
        # [0] - protoze tam jsou sequence
        # [-1] potrebuju posledni sequenci

        return np.array([preprocess_df(scraped_df, shuffle=False)[0][-1]])

    def predict_result(self, input_sample):
        return self.nn_model.predict(input_sample)

    def create_order(self, predikce, last_candle: CandleApi):
        if predikce == 1:
            tp: Decimal = last_candle.close_price * Decimal((1 + Config.TP / 100))
            sl: Decimal = last_candle.close_price * Decimal((1 - Config.SL / 100))
            self.manager.open_long(price=last_candle.close_price, take_profit=tp, stop_loss=sl)

        else:
            tp: Decimal = last_candle.close_price * Decimal((1 - Config.TP / 100))
            sl: Decimal = last_candle.close_price * Decimal((1 + Config.SL / 100))
            self.manager.open_short(price=last_candle.close_price, take_profit=tp, stop_loss=sl)

    def check_orders(self, last_candle):
        self.manager.check_opened_orders(last_candle)

    def print_profit(self):
        print(f"closed orders: {self.manager.closed_orders}, opened orders: {len(self.manager.opened_orders)} profitable_orders={self.manager.profitable_trades}")
        print(f"total profit: {round(self.manager.total_profit, 4)} %")
        print()

    def run(self):
        check_new_candle = False

        while True:
            now = datetime.now()
            # if now - time_compare > timedelta(minutes=Config.CANDLE_MINUTES_INTERVAL):
            if 2 < now.second < 5:      # zacatek kazde minuty s rezervou 2s
                check_new_candle = True

            if check_new_candle:
                last_candle: CandleApi

                scraped_candles, last_candle = self.scrape_candles()    # scraped candles, last candle in df
                preprocessed = self.preprocess_candles(scraped_candles=scraped_candles)
                predikce = self.predict_result(preprocessed)

                self.create_order(predikce=predikce, last_candle=last_candle)
                self.check_orders(last_candle)
                self.print_profit()
                check_new_candle = False
                time.sleep(50)

    @staticmethod
    def trade():
        live_trader = LiveTrading(symbol="BTCUSDT")
        live_trader.run()
