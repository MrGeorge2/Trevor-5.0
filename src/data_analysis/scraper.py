from ..globals.db import DB
from ..globals.config import Config
from ..api_handler.api_handler import ApiHandler
from binance.client import Client
from .models.candle_api import CandleApi
from typing import List
from datetime import datetime
from sqlalchemy import and_


class Scraper:
    def __init__(self):
        pass
    
    @staticmethod
    def scrape(symbol: str) -> None:
        print(f"SCRAPING {symbol}")
        global_i: DB = DB.get_globals()
        db = global_i.get_globals()

        api_handler: ApiHandler = ApiHandler.get_new_ApiHandler()

        scraped = api_handler.get_historical_klines(symbol, Config.CANDLE_INTERVAL, "1 DEC, 2010")
        for candle in scraped:
            m_candle: CandleApi = CandleApi(
                symbol=symbol,
                open_time=datetime.fromtimestamp(int(candle[0])/1000),
                open_price=candle[1],
                high_price=candle[2],
                low_price=candle[3],
                close_price=candle[4],
                volume=candle[5],
                close_time=datetime.fromtimestamp(int(candle[6])/1000),
                quote_asset_volume=candle[7],
                number_of_trades=candle[8],
                taker_buy_base_asset_volume=candle[9],
                taker_buy_quote_asset_volume=candle[10],
            )

            if Config.CHECK_ROW_IN_DB:
                if not db.SESSION.query(db.SESSION.query(CandleApi).filter(
                        and_(CandleApi.symbol == symbol, CandleApi.open_time == m_candle.open_time)).exists()).scalar():
                    db.SESSION.add(m_candle)
            else:
                db.SESSION.add(m_candle)

        db.SESSION.commit()
        print(f"Sraping {symbol} done")

    @staticmethod
    def scrape_all(*args):
        for symbol in Config.SYMBOLS_TO_SCRAPE:
            Scraper.scrape(symbol)


