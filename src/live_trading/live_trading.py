from ..globals.config import Config
from ..api_handler.api_handler import ApiHandler
from ..data_analysis.models.candle_api import CandleApi

from ..nn_model.modelnn import ModelNN
from ..samples.samples import Samples, preprocess_df
from ..data_analysis.models.candle_api import CandleApi
import pandas as pd
import numpy as np
import time

from datetime import datetime, timedelta
from .order import Long, Short
from .OrderManager import OrderManager


class LiveTrading:
    SIMULATION = Config.SIMULATION

    def __init__(self, symbol):
        self.nn_model = ModelNN()
        self.symbol = symbol
        self.manager = OrderManager(symbol=self.symbol)

    def scrape_candles(self):
        api_handler: ApiHandler = ApiHandler.get_new_ApiHandler()
        scraped = api_handler.get_historical_klines(self.symbol, Config.CANDLE_INTERVAL, "2 hour ago UTC")   #TODO: zkontrolovat casove pasmo
        candles = [CandleApi(open_price=candle[1], high_price=candle[2], low_price=candle[3], close_price=candle[4],
                             volume=candle[5]) for candle in scraped]

        open_price = float(candles[-1].open_price)
        high_price = float(candles[-1].high_price)
        low_price = float(candles[-1].low_price)
        close_price = float(candles[-1].close_price)
        return candles, open_price, high_price, low_price, close_price

    def preprocess_candles(self, scraped_candles):
        scraped_df = pd.DataFrame(candle.prices_as_dict_live() for candle in scraped_candles)
        # [0] - protoze tam jsou sequence
        # [-1] potrebuju posledni sequenci

        return np.array([preprocess_df(scraped_df, shuffle=False)[0][-1]])

    def predict_result(self, input_sample):
        return self.nn_model.predict(input_sample)

    def create_order(self, predikce, price):
        scraped_candles = self.scrape_candles()
        open_time = datetime.now()

        tp = price * (1 + Config.TP/100)
        sl = price * (1 - Config.SL/100)

        if predikce == 1:
            self.manager.open_long(price=price, take_profit=tp, stop_loss=sl)
        else:
            self.manager.open_short(price=price, take_profit=tp, stop_loss=sl)

    def check_orders(self, open_price, high_price, low_price, close_price, actual_time):
        for order in self.manager.opened_orders:
            if (actual_time - order.init_order.open_time) >= timedelta(minutes=Config.CANDLE_MINUTES_INTERVAL):
                order.close()

                self.CLOSED_ORDERS.append(order)
                self.OPEN_ORDERS.pop((self.OPEN_ORDERS.index(order)))

            else:
                if order.UP == 1:
                    if ((order.OPEN_PRICE - low_price) / order.OPEN_PRICE) * 100 > order.LIMIT:
                        order.close(close_price=(order.OPEN_PRICE) * (1 - (order.LIMIT/100)))

                    if ((high_price - order.OPEN_PRICE) / order.OPEN_PRICE) * 100 > order.LIMIT:
                        order.close(close_price=(order.OPEN_PRICE) * (1 + (order.LIMIT/100)))

                    self.CLOSED_ORDERS.append(order)
                    self.OPEN_ORDERS.pop((self.OPEN_ORDERS.index(order)))

                if order.UP == 0:
                    if ((high_price - order.OPEN_PRICE) / order.OPEN_PRICE) * 100 > order.LIMIT:
                        order.close(close_price=(order.OPEN_PRICE) * (1 - (order.LIMIT/100)))

                    if ((order.OPEN_PRICE - low_price) / order.OPEN_PRICE) * 100 > order.LIMIT:
                        order.close(close_price=(order.OPEN_PRICE) * (1 + (order.LIMIT/100)))

                    self.CLOSED_ORDERS.append(order)
                    self.OPEN_ORDERS.pop((self.OPEN_ORDERS.index(order)))

    def count_profit(self):
        profit_counter = 0
        for order in self.CLOSED_ORDERS:
            profit_counter += order.get_profit()
        print(f"open orders: {len(self.OPEN_ORDERS)}, closed orders: {len(self.CLOSED_ORDERS)}")
        print(f"total profit from all closed orders is {profit_counter} %")

    def run(self):
        time_compare = datetime.now()
        check_new_candle = False

        while True:
            now = datetime.now()
            # if now - time_compare > timedelta(minutes=Config.CANDLE_MINUTES_INTERVAL):
            if now.second < 5:
                check_new_candle = True

            if check_new_candle:
                scraped_candles, open_price, high_price, low_price, close_price = self.scrape_candles() #prices for last candle in df
                preprocessed = self.preprocess_candles(scraped_candles=scraped_candles)
                predikce = self.predict_result(preprocessed)
                self.create_order(predikce=predikce, price=close_price)
                self.check_orders(high_price, close_price, low_price, close_price, actual_time=datetime.now())
                self.count_profit()
                check_new_candle = False
                time.sleep(50)

    @staticmethod
    def trade():
        live_trader = LiveTrading(symbol="BTCUSDT")
        live_trader.run()
