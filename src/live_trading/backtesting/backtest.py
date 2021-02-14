from src.globals.config import Config
from ..base.trading_base import TradingInterface
from ...api_handler.api_handler import ApiHandler
import logging
from numpy import median, mean
from ...data_analysis.models.views import ViewWithtRes, ViewTypeWithRes


class BackTest(TradingInterface):

    def __init__(self, symbol):
        super().__init__(symbol)

    def run(self):
        api_handler = ApiHandler.get_new_ApiHandler()

        def scraper_func():
            return api_handler.get_historical_klines(self.symbol, Config.CANDLE_INTERVAL, "7 day ago UTC")
            # return api_handler.futures_klines(symbol=self.symbol, interval=Config.CANDLE_INTERVAL)

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


            up, down = self._predict_result(preprocessed)
            logging.info(f"tp={up} Predikce={down} Delta={self.delta}")

            if self.delta >= Config.MINIMAL_DELTA:
                self._create_order(last_candle=last_candle, up=up, down=down)

            logging.info(" ")  # Prazdny loger je tu spravne

        logging.info(f"Backtestesting DONE,\t"
                     f"number of trades: {self.manager.closed_orders},\t"
                     f"total net profit: {self.total_net_profit} %,\t"
                     f"net profit per trade: {self.net_profit_per_trade} %,\t"
                     f"trading time: {str(self.trading_time)} ")

    def analyze_avg_percent_changes_sl_tp(self):
        max_drops = []
        max_raises = []
        test_data = ViewWithtRes.get_train_candles_for_symbol(self.symbol)
        for i in range(len(test_data)):
            if i + Config.NUMBER_FUTURE_CANDLE_PREDICT >= len(test_data):
                break

            act_drop = 0
            act_raise = 0

            act_candle = test_data[i]
            for iter_candle in test_data[i + 1: i + Config.NUMBER_FUTURE_CANDLE_PREDICT]:
                temp_drop = ((iter_candle.low_price - act_candle.open_price) * 100) / act_candle.open_price
                temp_raise = ((iter_candle.close_price - act_candle.open_price) * 100) / act_candle.open_price

                if temp_drop < act_drop:
                    act_drop = temp_drop

                if temp_raise > act_raise:
                    act_raise = temp_raise

            max_drops.append(act_drop)
            max_raises.append(act_raise)

        avg_drop = mean(max_drops)
        median_drop = median(max_drops)

        avg_raise = mean(max_raises)
        median_raise = median(max_raises)

        print(f"avg_drop={avg_drop} median_drop={median_drop} avg_raise={avg_raise} median_raise={median_raise}")
        return avg_drop, median_drop, avg_raise, median_raise


def backtest():
    backtester = BackTest("MKRUSDT")
    backtester.analyze_avg_percent_changes_sl_tp()
    backtester.run()
