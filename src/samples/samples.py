from ..globals.config import Config
from ..data_analysis.models.views import ViewWithtRes
import tensorflow as tf
from ..data_analysis.models.candle_api import CandleApi
from ..globals.db import DB
from sqlalchemy import Table, Column, Integer, String, DATETIME, DECIMAL, Boolean
from typing import List
import random
import tensorflow as tf


class Samples(ViewWithtRes):

    @staticmethod
    def create_samples():
        db = DB.get_globals()
        for symbol in random.sample(Config.SYMBOLS_TO_SCRAPE, Config.RANDOM_SYMBOLS_FOR_SAMPLE):
            print(f"Creating samples from symbol={symbol}")

            candles: List[ViewWithtRes] = db.SESSION.query(ViewWithtRes).filter(ViewWithtRes.symbol == symbol)
            empty_variable = tf.zeros(shape=(1, 1, Config.NUMBER_OF_COLUMNS - 1))

            for i, candle in enumerate(candles):
                pomocna = tf.zeros(shape=(1, 1, Config.NUMBER_OF_COLUMNS - 1))
                
                open_time = candle.open_time
                open_price = candle.open_price
                high_price = candle.high_price
                low_price = candle.low_price
                close_price = candle.close_price
                volume = candle.volume
                close_time = candle.close_price
                quote_asset_volume = candle.quote_asset_volume
                number_of_trades = candle.number_of_trades
                taker_buy_base_asset_volume = candle.taker_buy_base_asset_volume
                taker_buy_quote_asset_volume = candle.taker_buy_quote_asset_volume
                sma21 = candle.sma21
                sma200 = candle.sma200
                ema21 = candle.ema21
                ema200 = candle.ema200
                up = candle.up
                down = candle.down


                print(open_time)
