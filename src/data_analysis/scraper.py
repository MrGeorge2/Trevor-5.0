from ..api_handler.api_handler import ApiHandler
from binance.client import Client
from .models.candle_api import CandleApi
from typing import List

class Scraper:
    def __init__(self):
        pass
    
    @staticmethod
    def scrape(symbol: str) -> None:
        apiHandler:ApiHandler = ApiHandler.get_new_ApiHandler()
        scraped = apiHandler.get_historical_klines(symbol, Client.KLINE_INTERVAL_4HOUR, "1 DEC, 2010")
        scrapedCandles: List[CandleApi] = []
        for candle in scraped:
            m_candle: CandleApi = CandleApi(
                open_time=candle[0],
                open_price=candle[1],
                high_price=candle[2],
                low_price=candle[3],
                close_price=candle[4],
                volume=candle[5],
                close_time=candle[6],
                quote_asset_volume=[7],
                number_of_trades=[8],
                taker_buy_base_asset_volume=[9],
                taker_buy_quote_asset_volume=[10],
            )
            scrapedCandles.append(m_candle)
        print()
        print(scrapedCandles)
        


