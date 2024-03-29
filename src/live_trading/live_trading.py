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

        def scraper_func():
            return api_handler.futures_klines(symbol=self.symbol, interval=Config.CANDLE_INTERVAL)

        check_new_candle = False

        while True:
            now = datetime.now()
            # if now - time_compare > timedelta(minutes=Config.CANDLE_MINUTES_INTERVAL):
            if 2 < now.second < 5 and now.minute % 15 == 0:      # zacatek kazde minuty s rezervou 2s
                check_new_candle = True

            if check_new_candle:
                last_candle: CandleApi
                try:
                    scraped_candles, last_candle = self._scrape_candles(scraper_func)    # scraped candles, last candle in df
                except Exception as e:
                    logging.critical(e)
                    continue

                self._check_orders(last_candle, last_candle.close_time) # TODO: NEMELO BY TO BYT AZ PO NACTENI DALSICH SVICEK?
                self._print_profit()

                preprocessed = self._preprocess_candles(scraped_candles=scraped_candles)

                predikce, jistota = self._predict_result(preprocessed)
                logging.info(f"Jistota={jistota} Predikce={predikce} Delta={self.delta}")

                if self.delta >= Config.MINIMAL_DELTA and jistota >= 6:
                    self._create_order(prediction=predikce, last_candle=last_candle)

                logging.info(" ")  # Prazdny loger je tu spravne

                check_new_candle = False
                time.sleep(890)

    @staticmethod
    def trade():
        live_trader = LiveTrading(symbol="MKRUSDT")
        live_trader.run()
