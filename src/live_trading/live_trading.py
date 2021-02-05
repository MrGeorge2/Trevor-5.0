from ..globals.config import Config
from ..data_analysis.models.candle_api import CandleApi
import time
from datetime import datetime
import logging
from .base.trading_base import TradingInterface
from ..api_handler.api_handler import ApiHandler


class LiveTrading(TradingInterface):
    SIMULATION = Config.SIMULATION

    def __init__(self, symbol):
        super().__init__(symbol)

    def run(self):
        api_handler: ApiHandler = ApiHandler.get_new_ApiHandler()
        check_new_candle = False

        while True:
            now = datetime.now()
            # if now - time_compare > timedelta(minutes=Config.CANDLE_MINUTES_INTERVAL):
            if 2 < now.second < 5:      # zacatek kazde minuty s rezervou 2s
                check_new_candle = True

            if check_new_candle:
                last_candle: CandleApi
                try:
                    scraped_candles, last_candle = self._scrape_candles(api_handler.futures_klines)    # scraped candles, last candle in df
                except Exception as e:
                    logging.critical(e)
                    continue

                preprocessed = self._preprocess_candles(scraped_candles=scraped_candles)

                predikce, jistota = self._predict_result(preprocessed)
                logging.info(f"Jistota={jistota} Predikce={predikce} Delta={self.delta}")

                if self.delta >= Config.MINIMAL_DELTA:
                    self._create_order(prediction=predikce, last_candle=last_candle)

                self._check_orders(last_candle)
                self._print_profit()
                check_new_candle = False
                time.sleep(50)

    @staticmethod
    def trade():
        live_trader = LiveTrading(symbol="ETHUSDT")
        live_trader.run()
