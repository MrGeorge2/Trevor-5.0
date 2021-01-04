from ..globals.config import Config
from ..data_analysis.models.views import ViewWithtRes, ViewTypeWithRes
from ..globals.db import DB
from sqlalchemy import Table, Column, Integer, String, DATETIME, DECIMAL, Boolean, asc
from typing import List
import random
import tensorflow as tf
import numpy as np


class Samples:
    def __init__(self, symbol):
        self.symbol = symbol
        self.candles:  List[ViewTypeWithRes] = []

    def get_candles(self):
        db = DB.get_globals()
        self.candles = db.SESSION.query(ViewWithtRes).filter(
            ViewWithtRes.symbol == self.symbol).order_by(
            asc(ViewWithtRes.open_time)).all()  # pred .all() .limit(100)

    def count2d_samples(self):
        pass

    def count3d_samples(self):
        pass

    def normalize(self):
        pass

    def normalize_time(self, dt):
        """0-24 hod do rozsahu 0-1"""
        normalized_time = float(dt.hour*3600+dt.minute*60+dt.second)/86400
        return normalized_time

    def create_samples_for_symbol(self):
        self.get_candles()
        tabulka_jedne_meny = np.zeros(shape=(1, Config.NUMBER_OF_SAMPLE_COLUMNS))

        for i, candle in enumerate(self.candles):
            radek = np.zeros(shape=(1, Config.NUMBER_OF_SAMPLE_COLUMNS))

            radek[0, 0] = self.normalize_time(candle.open_time)
            radek[0, 1] = candle.open_price
            radek[0, 2] = candle.high_price
            radek[0, 3] = candle.low_price
            radek[0, 4] = candle.close_price
            radek[0, 5] = candle.volume
            radek[0, 6] = candle.quote_asset_volume
            radek[0, 7] = candle.number_of_trades
            radek[0, 8] = candle.taker_buy_base_asset_volume
            radek[0, 9] = candle.taker_buy_quote_asset_volume
            radek[0, 10] = candle.sma21
            radek[0, 11] = candle.sma200
            radek[0, 12] = candle.ema21
            radek[0, 13] = candle.ema200
            radek[0, 14] = candle.up
            radek[0, 15] = candle.down

            tabulka_jedne_meny = np.concatenate((tabulka_jedne_meny, radek), axis=0)
        tabulka_jedne_meny = tabulka_jedne_meny[1:, :]
        x=10


    @classmethod
    def get_sample_cls(cls, symbol):
        return Samples(symbol)

    @staticmethod
    def create_samples():
        for symbol in random.sample(Config.SYMBOLS_TO_SCRAPE, Config.RANDOM_SYMBOLS_FOR_SAMPLE):
            print(f"Creating samples from symbol={symbol}")

            samples = Samples.get_sample_cls(symbol)
            result_samples = samples.create_samples_for_symbol()
