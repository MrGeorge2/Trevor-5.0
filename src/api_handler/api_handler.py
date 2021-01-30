from binance.client import Client
from ..globals.config import Config
from datetime import datetime


class ApiHandler(Client):
    def __init__(self, cfg: Config):
        super().__init__(cfg.API_KEY, cfg.S_KEY, {"verify": True, "timeout": 2000000})
        self._config: Config = cfg
    
    @classmethod
    def get_new_ApiHandler(cls):
        return cls(cfg=Config())


if __name__ == '__main__':
    cfg = Config()
    apiHandler = ApiHandler.get_new_ApiHandler()

    # api_handler.check_if_actual_symbol_pumping()
