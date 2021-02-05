from src.globals.config import Config
from ..base.trading_base import TradingInterface
from src.live_trading.live_trading import LiveTrading
from datetime import timedelta
from decimal import Decimal
import logging


class BackTest(TradingInterface):

    def __init__(self, symbol):
        super().__init__(symbol)

    def run(self):
        backtesting_data = self._scrape_candles(Config.NUMBER_OF_TESTING_CANDLES)

        for i in range(len(backtesting_data) - Config.TIMESTEPS - 200):
            logging.info(f"Backtest: {i}/{len(backtesting_data)},\t"
                  f"number of trades: {self.manager.closed_orders},\t"
                  f"total net profit: {self.total_net_profit},\t"
                  f"net profit per trade: {self.net_profit_per_trade}")

            actual_sample = backtesting_data[i: i+Config.TIMESTEPS+200]
            last_candle = actual_sample[-1]
            preprocessed = self._preprocess_candles(scraped_candles=actual_sample)

            predikce, jistota = self._predict_result(preprocessed)
            logging.info(f"Jistota={jistota} Predikce={predikce} Delta={self.delta}")

            if self.delta >= Config.MINIMAL_DELTA:
                self._create_order(prediction=predikce, last_candle=last_candle)

            self._check_orders(last_candle)
            self._print_profit()

        logging.info(f"Backtestesting DONE,\t"
                     f"number of trades: {self.manager.closed_orders},\t"
                     f"total net profit: {self.total_net_profit},\t"
                     f"net profit per trade: {self.net_profit_per_trade}")


def backtest():
    backtester = BackTest("BTCUSDT")
    backtester.run()
