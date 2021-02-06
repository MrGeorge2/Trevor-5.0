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
            return api_handler.get_historical_klines(self.symbol, Config.CANDLE_INTERVAL, "7 day ago UTC")

        backtesting_data, _ = self._scrape_candles(scraper_func=scraper_func)

        for i in range(len(backtesting_data) - Config.TIMESTEPS + (500 - Config.TIMESTEPS)):
            simulation_time = datetime.now() - timedelta(minutes=((len(backtesting_data) - Config.TIMESTEPS + (500 - Config.TIMESTEPS)) - i))

            logging.info(f"Backtest: {i}/{len(backtesting_data)},\t"
                         f"number of trades: {self.manager.closed_orders},\t"
                         f"total net profit: {self.total_net_profit},\t"
                         f"net profit per trade: {self.net_profit_per_trade}")

            actual_sample = backtesting_data[i: i + Config.TIMESTEPS + (500 - Config.TIMESTEPS)]
            last_candle = actual_sample[-1]
            self._check_orders(last_candle, checktime=simulation_time)
            self._print_profit()

            preprocessed = self._preprocess_candles(scraped_candles=actual_sample)

            predikce, jistota = self._predict_result(preprocessed)
            logging.info(f"Jistota={jistota} Predikce={predikce} Delta={self.delta}")

            pocet_otevrenych_obchodu = len(self.manager.opened_orders)
            if self.delta >= Config.MINIMAL_DELTA:
                self._create_order(prediction=predikce, last_candle=last_candle)
                if len(self.manager.opened_orders) > pocet_otevrenych_obchodu:
                    self.manager.opened_orders[-1].init_order.open_time = simulation_time

        logging.info(f"Backtestesting DONE,\t"
                     f"number of trades: {self.manager.closed_orders},\t"
                     f"total net profit: {self.total_net_profit},\t"
                     f"net profit per trade: {self.net_profit_per_trade}")


def backtest():
    backtester = BackTest("BTCUSDT")
    backtester.run()
