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
from .order_manager import OrderManager
import logging
from .base.trading_base import TradingInterface


class LiveTrading(TradingInterface):
    SIMULATION = Config.SIMULATION

    def __init__(self, symbol):
        super().__init__(symbol)

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
                    scraped_candles, last_candle = self._scrape_candles()    # scraped candles, last candle in df
                except Exception as e:
                    logging.critical(e)

                preprocessed = self._preprocess_candles(scraped_candles=scraped_candles)

                predikce, jistota = self._predict_result(preprocessed)

                logging.info(f"Jistota={jistota} predikce={predikce}")
                if jistota >= 0.70:
                    self._create_order(prediction=predikce, last_candle=last_candle)

                self._check_orders(last_candle)
                self._print_profit()
                check_new_candle = False
                time.sleep(50)

    @staticmethod
    def trade():
        live_trader = LiveTrading(symbol="BTCUSDT")
        live_trader.run()
