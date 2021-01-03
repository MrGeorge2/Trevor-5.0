from ..globals.config import Config
from ..data_analysis.models.views import ViewWithtRes, ViewTypeWithRes
from ..globals.db import DB
from sqlalchemy import Table, Column, Integer, String, DATETIME, DECIMAL, Boolean, asc
from typing import List
import random
import tensorflow as tf
import numpy as np


class Samples:


    @staticmethod
    def create_samples():
        db = DB.get_globals()
        for symbol in random.sample(Config.SYMBOLS_TO_SCRAPE, Config.RANDOM_SYMBOLS_FOR_SAMPLE):
            print(f"Creating samples from symbol={symbol}")

            candles: List[ViewTypeWithRes] = db.SESSION.query(ViewWithtRes).filter(ViewWithtRes.symbol == symbol).order_by(
                asc(ViewWithtRes.open_time)).limit(100).all()

            tabulka_jedne_meny = tf.zeros(shape=(1, 1, Config.NUMBER_OF_COLUMNS - 1))

            radek = np.zeros(shape=(1, 1, Config.NUMBER_OF_COLUMNS - 1))
            for i, candle in enumerate(candles):
                radek[1, 1, 0] = candle.open_time
                radek[1, 1, 1] = candle.open_price
                radek[1, 1, 2] = candle.high_price
                radek[1, 1, 3] = candle.low_price
                radek[1, 1, 4] = candle.close_price
                radek[1, 1, 5] = candle.volume
                radek[1, 1, 6] = candle.close_price
                radek[1, 1, 7] = candle.quote_asset_volume
                radek[1, 1, 8] = candle.number_of_trades
                radek[1, 1, 9] = candle.taker_buy_base_asset_volume
                radek[1, 1, 10] = candle.taker_buy_quote_asset_volume
                radek[1, 1, 11] = candle.sma21
                radek[1, 1, 12] = candle.sma200
                radek[1, 1, 13] = candle.ema21
                radek[1, 1, 14] = candle.ema200
                radek[1, 1, 15] = candle.up
                radek[1, 1, 16] = candle.down
                tabulka_jedne_meny = tf.concat([tabulka_jedne_meny, tf.Variable(radek)], axis=1)
            tabulka_jedne_meny = tabulka_jedne_meny[1, 1:, :]

            print(" a ")
