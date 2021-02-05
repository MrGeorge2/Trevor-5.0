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
