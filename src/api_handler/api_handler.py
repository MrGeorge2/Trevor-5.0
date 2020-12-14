from __future__ import annotations
from binance.client import Client
from ..config import Config
from datetime import datetime


class ApiHandler(Client):
    def __init__(self, cfg: Config):
        super().__init__(cfg.API_KEY, cfg.S_KEY, {"verify": True})
        self._config: Config = cfg
    
    @classmethod
    def get_new_ApiHandler(cls) -> ApiHandler:
        return cls(cfg=Config())

    @staticmethod
    def run():
        result = ApiHandler.get_new_ApiHandler().get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_4HOUR, "1 DEC, 2010")
        print(result)

    
if __name__ == '__main__':
    cfg = Config()
    apiHandler = ApiHandler.get_new_ApiHandler()

    # api_handler.check_if_actual_symbol_pumping()
