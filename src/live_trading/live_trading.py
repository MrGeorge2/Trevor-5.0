from ..globals.config import Config
from ..api_handler.api_handler import ApiHandler
from ..data_analysis.models.candle_api import CandleApi

from ..nn_model.modelnn import ModelNN
from ..samples.samples import Samples, preprocess_df
from ..data_analysis.models.candle_api import CandleApi
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from .order import Long, Short


class LiveTrading:
    OPEN_ORDERS = []
    CLOSED_ORDERS = []

    SIMULATION = Config.SIMULATION

    def __init__(self, symbol):
        self.NN_MODEL = ModelNN()
        self.SYMBOL = symbol

    def scrape_candles(self):
        api_handler: ApiHandler = ApiHandler.get_new_ApiHandler()
        scraped = api_handler.get_historical_klines(self.SYMBOL, Config.CANDLE_INTERVAL, "2 hour ago UTC")   #TODO: zkontrolovat casove pasmo
        candles = [CandleApi(open_price=candle[1], high_price=candle[2], low_price=candle[3], close_price=candle[4],
                             volume=candle[5]) for candle in scraped]

        open_price = candles[:-1, 1]
        high_price = candles[:-1, 2]
        low_price = candles[:-1, 3]
        close_price = candles[:-1, 4]
        return candles, open_price, high_price, low_price, close_price

    def preprocess_candles(self, scraped_candles):
        scraped_df = pd.DataFrame(candle.prices_as_dict_live() for candle in scraped_candles)
        # [0] - protoze tam jsou sequence
        # [-1] potrebuju posledni sequenci

        return np.array([preprocess_df(scraped_df, shuffle=False)[0][-1]])

    def predict_result(self, input_sample):
        return self.NN_MODEL.predict(input_sample)

    def create_order(self, predikce, order_open_price):
        scraped_candles = self.scrape_candles()
        open_time = datetime.now()
        if predikce == 1:
            order = Long(open_price=order_open_price)
        else:
            order = Short(open_price=order_open_price)

        self.OPEN_ORDERS.append(order)

    def check_orders(self, actual_time, open_price, high_price, low_price, close_price):
        for order in self.OPEN_ORDERS:
            if (order.OPEN_TIME - actual_time) > timedelta(minutes=12):
                order.close(close_price=high_price)

                self.CLOSED_ORDERS.append(order)
                self.OPEN_ORDERS.pop(order)

            else:
                if order.UP == 1:
                    if ((open_price - order.OPEN_PRICE) / order.OPEN_PRICE) > order.LIMIT:
                        order.close(close_price=open_price)

                        self.CLOSED_ORDERS.append(order)
                        self.OPEN_ORDERS.pop(order)
                if order.UP == 0:
                    if ((order.OPEN_PRICE - open_price) / order.OPEN_PRICE) > order.LIMIT:
                        order.close(close_price=open_price)

                        self.CLOSED_ORDERS.append(order)
                        self.OPEN_ORDERS.pop(order)

    def count_profit(self):
        profit_counter = 0
        for order in self.CLOSED_ORDERS:
            profit_counter += order.get_profit()
        print(f"total profit from all closed orders is {profit_counter} %")

    def run(self):
        check_new_candle = True
        now = datetime.now()
        if check_new_candle:
            scraped_candles, open_price, high_price, low_price, close_price = self.scrape_candles() #prices for last candle in df
            preprocessed = self.preprocess_candles(scraped_candles=scraped_candles)
            predikce = self.predict_result(preprocessed)
            self.create_order(predikce=predikce, order_open_price=close_price)
            self.check_orders(high_price, close_price, low_price, close_price)
            self.count_profit()

        return 0

    @staticmethod
    def trade():
        live_trader = LiveTrading()
        live_trader.run()
