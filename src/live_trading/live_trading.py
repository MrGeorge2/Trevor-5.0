from ..globals.config import Config
from ..api_handler.api_handler import ApiHandler
from ..data_analysis.models.candle_api import CandleApi

from ..nn_model.modelnn import ModelNN
from ..samples.samples import Samples, preprocess_df
from .order import Order
from datetime import datetime
import pandas as pd
import numpy as np


class LiveTrading:
    OPEN_ORDERS = []
    CLOSED_ORDERS = []

    SIMULATION = Config.SIMULATION

    def __init__(self):
        self.NN_MODEL = ModelNN()

    def scrape_candles(self, symbol):
        api_handler: ApiHandler = ApiHandler.get_new_ApiHandler()
        scraped = api_handler.get_historical_klines(symbol, Config.CANDLE_INTERVAL, "1 hour ago UTC")   #TODO: zkontrolovat casove pasmo
        return scraped

    def preprocess_candles(self, scraped_candles):
        sc = scraped_candles
        df = pd.DataFrame(scraped_candles)
        return preprocess_df(df, shuffle=False)

    def predict_result(self, input_sample):
        self.NN_MODEL.predict(input_sample)

    def create_order(self):
        pass

    def check_orders(self):
        pass

    def run(self):
        scraped_candles = self.scrape_candles("BTCUSDT")
        sc = self.preprocess_candles(scraped_candles=scraped_candles)
        return 0

    @staticmethod
    def trade():
        live_trader = LiveTrading()
        live_trader.run()
