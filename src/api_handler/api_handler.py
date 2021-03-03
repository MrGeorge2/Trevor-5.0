from ftx import FtxClient
from ..globals.config import Config
from datetime import datetime, timedelta
import math


class ApiHandler(FtxClient):
    def __init__(self):
        self._config: Config = Config()
        super().__init__(api_key=self._config.API_KEY, api_secret=self._config.S_KEY)

    def get_candles(self, start_time: datetime, end_time: datetime, symbol: str = Config.SYMBOL):
        # TODO: JE TAM POSUN O HODINU.... max 5000 svicek najednou
        limit = math.floor((end_time.timestamp() - start_time.timestamp()) / self._config.CANDLE_INTERVAL)
        candles = self.get_historical_data(market_name=symbol, resolution=self._config.CANDLE_INTERVAL, limit=limit, start_time=start_time.timestamp(), end_time=end_time.timestamp())
        return candles

    def get_all_candles(self, symbol):
        start_date = datetime(year=2017, month=1, day=1, hour=0)
        end_date = datetime.now()
        number_of_candles = math.floor(end_date.timestamp() - start_date.timestamp()) / self._config.CANDLE_INTERVAL
        max_candles = 5000  # tolik jde najednou stahnout z ftx

        tmp_date = start_date
        all_candles = []

        for interval in range(number_of_candles/max_candles):
            all_candles.append(self.get_candles(start_time=tmp_date, end_time=tmp_date+timedelta(minutes=max_candles*(self._config.CANDLE_INTERVAL/60))))
            tmp_date += timedelta(minutes=max_candles*(self._config.CANDLE_INTERVAL/60))

        return all_candles

    def __get_delta_for_symbol(self, symbol: str) -> float:
        candles = self.get_market(market=Config.SYMBOL)
        last_candle = candles[-1]

        last_high = float(last_candle[2])
        last_low = float(last_candle[3])

        last_open = float(last_candle[1])
        last_close = float(last_candle[4])

        if last_close < last_open or last_close < self._config.MINIMAL_PRICE:
            return 0.0

        delta = (last_high - last_low) / last_high
        return delta * 100

    @classmethod
    def get_new_ApiHandler(cls):
        return cls()


class ApiTest:
    @staticmethod
    def test_ftx_api():
        api_handler = ApiHandler()
        candles = api_handler.get_candles(start_time=datetime(year=2021, month=1, day=10, hour=18), end_time=datetime.now())
        print(f"prvni: {candles[0]}, posledni: {candles[-1]}")
        return 0

"""
from binance.client import Client
from ..globals.config import Config
from datetime import datetime


class ApiHandler(Client):
    def __init__(self, cfg: Config):
        super().__init__(cfg.API_KEY, cfg.S_KEY, {"verify": True, "timeout": 2000000})
        self._config: Config = cfg

    def __get_delta_for_symbol(self, symbol: str) -> float:
        candles = self.get_historical_klines(symbol=symbol, interval=self.KLINE_INTERVAL_15MINUTE, start_str="4 hours ago")
        last_candle = candles[-1]

        last_high = float(last_candle[2])
        last_low = float(last_candle[3])

        last_open = float(last_candle[1])
        last_close = float(last_candle[4])

        if last_close < last_open or last_close < self.config.MINIMAL_PRICE:
            return 0.0

        delta = (last_high - last_low) / last_high
        return delta * 100
    
    @classmethod
    def get_new_ApiHandler(cls):
        return cls(cfg=Config())


if __name__ == '__main__':
    cfg = Config()
    apiHandler = ApiHandler.get_new_ApiHandler()

    # api_handler.check_if_actual_symbol_pumping()
"""
