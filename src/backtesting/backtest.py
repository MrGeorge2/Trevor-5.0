from ..globals.config import Config
from ..data_analysis.models.views import ViewWithtRes, ViewTypeWithRes
from typing import List
from numpy import mean, median, argmax, reshape
from ..nn_model.modelnn import ModelNN
from ..samples.samples import Samples
from ..live_trading.live_trading import LiveTrading
from datetime import timedelta
from decimal import Decimal


class BackTestInterface:
    TOTAL_PROFIT: Decimal = 0
    NUMBER_OF_TRADES: int = 0
    TRADING_TIME_MINUTES: int = 0    # minutes

    @property
    def total_net_profit(self) -> Decimal:
        return self.TOTAL_PROFIT - (self.NUMBER_OF_TRADES * Config.FEE * 2)

    @property
    def net_profit_per_trade(self) -> Decimal:
        return self.total_net_profit / self.NUMBER_OF_TRADES

    @property
    def trading_time(self) -> timedelta:
        return timedelta(minutes=self.TRADING_TIME_MINUTES)


class BackTest(BackTestInterface):
    def __init__(self):
        self.live_trader = LiveTrading(symbol=Config.SYMBOL_LIVE_TRADING)
        self.backtesting_data, _ = self.live_trader.scrape_candles(limit=Config.NUMBER_OF_TESTING_CANDLES)

    def backtest(self):

        for i in range(len(self.backtesting_data) - Config.TIMESTEPS):
            print(f"Backtest: {i}/{len(self.backtesting_data)},   total net profit: {self.total_net_profit},  net profit per trade: {self.net_profit_per_trade}")
            actual_sample = self.backtesting_data[i: i+Config.TIMESTEPS]

            if self.live_trader.process_candle(timesteps_to_process=actual_sample):
                self.TOTAL_PROFIT = self.live_trader.manager.total_profit

        print(f"Backtestesting DONE,   total net profit: {self.total_net_profit},  net profit per trade: {self.net_profit_per_trade}")


def backtest():
    backtester = BackTest()
    backtester.backtest()
