from ..globals.config import Config
from ..data_analysis.models.views import ViewWithtRes
import tensorflow as tf
from ..data_analysis.models.candle_api import CandleApi
from ..globals.db import DB
from sqlalchemy import Table, Column, Integer, String, DATETIME, DECIMAL, Boolean
from typing import List
import random


class Samples(ViewWithtRes):

    @staticmethod
    def create_samples():
        db = DB.get_globals()
        for symbol in random.sample(Config.SYMBOLS_TO_SCRAPE, Config.RANDOM_SYMBOLS_FOR_SAMPLE):
            print(f"Creating samples from symbol={symbol}")

            
            candles: List[CandleApi] = db.SESSION.query(CandleApi).filter(CandleApi.symbol == symbol)
            """
            for i, candle in enumerate(candles):
                open_price = candle.open_price
                close_price = candle.close_price

                if Config.CHECK_ROW_IN_DB:

                    if not db.SESSION.query(db.SESSION.query(Results).filter(
            """
            print(candles)