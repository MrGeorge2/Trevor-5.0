from ..globals.config import Config
from ..api_handler.api_handler import ApiHandler
from ..data_analysis.models.candle_api import CandleApi

from ..nn_model.modelnn import ModelNN
from ..samples.samples import Samples, preprocess_df
from ..data_analysis.models.candle_api import CandleApi
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
        scraped = api_handler.get_historical_klines(symbol, Config.CANDLE_INTERVAL, "2 hour ago UTC")   #TODO: zkontrolovat casove pasmo
        candles = [CandleApi(open_price=candle[1], high_price=candle[2], low_price=candle[3], close_price=candle[4],
                             volume=candle[5]) for candle in scraped]
        return candles

    def preprocess_candles(self):
        scraped_candles = self.scrape_candles("BTCUSDT")
        scraped_df = pd.DataFrame(candle.prices_as_dict_live() for candle in scraped_candles)
        # [0] - protoze tam jsou sequence
        # [-1] potrebuju posledni sequenci
        return np.array([preprocess_df(scraped_df, shuffle=False)[0][-1]])

    def predict_result(self, input_sample):
        return self.NN_MODEL.predict(input_sample)

    def create_order(self):
        pass

    def check_orders(self):
        pass

    def run(self):
        preprocessed = self.preprocess_candles()
        predikce = self.predict_result(preprocessed)
        return 0

    @staticmethod
    def trade():
        live_trader = LiveTrading()
        live_trader.run()
