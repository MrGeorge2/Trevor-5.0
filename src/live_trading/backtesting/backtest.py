from src.globals.config import Config
from ..base.trading_base import TradingInterface
from ...api_handler.api_handler import ApiHandler
import logging
from datetime import datetime, timedelta


class BackTest(TradingInterface):

    def __init__(self, symbol):
        super().__init__(symbol)

    def run(self):
        api_handler = ApiHandler.get_new_ApiHandler()

        def scraper_func():
            return api_handler.get_historical_klines(self.symbol, Config.CANDLE_INTERVAL, "1 day ago UTC")

        backtesting_data, last_candle = self._scrape_candles(scraper_func=scraper_func)

        for i in range(len(backtesting_data) - 2 * Config.TIMESTEPS - 1): # + (500 - Config.TIMESTEPS)):
            self._update_trading_time(last_candle=last_candle)

            logging.info(f"Backtest: {i}/{len(backtesting_data)},\t"
                         f"number of trades: {self.manager.closed_orders},\t"
                         f"total net profit: {self.total_net_profit} %,\t"
                         f"net profit per trade: {self.net_profit_per_trade} %,\t"
                         f"trading time: {str(self.trading_time)}")

            actual_sample = backtesting_data[i: i + 2 * Config.TIMESTEPS - 1]
            last_candle = actual_sample[-1]
            self._check_orders(last_candle, checktime=last_candle.close_time)
            self._print_profit()

            preprocessed = self._preprocess_candles(scraped_candles=actual_sample)

            predikce, jistota = self._predict_result(preprocessed)
            logging.info(f"Jistota={jistota} Predikce={predikce} Delta={self.delta}")

            if self.delta >= Config.MINIMAL_DELTA:
                self._create_order(prediction=predikce, last_candle=last_candle)

        logging.info(f"Backtestesting DONE,\t"
                     f"number of trades: {self.manager.closed_orders},\t"
                     f"total net profit: {self.total_net_profit} %,\t"
                     f"net profit per trade: {self.net_profit_per_trade} %,\t"
                     f"trading time: {str(self.trading_time)} ")


def backtest():
    backtester = BackTest("BTCUSDT")
    backtester.run()
