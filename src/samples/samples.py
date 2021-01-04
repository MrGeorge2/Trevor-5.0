from ..globals.config import Config
from ..data_analysis.models.views import ViewWithtRes, ViewTypeWithRes
from ..globals.db import DB
from sqlalchemy import Table, Column, Integer, String, DATETIME, DECIMAL, Boolean, asc
from typing import List
import random
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import math

class Samples:
    def __init__(self, symbol):
        self.symbol = symbol
        self.candles:  List[ViewTypeWithRes] = []

    def get_candles(self):
        db = DB.get_globals()
        self.candles = db.SESSION.query(ViewWithtRes).filter(
            ViewWithtRes.symbol == self.symbol).order_by(
            asc(ViewWithtRes.open_time)).all()  # pred .all() .limit(100)

    def create3d_samples(self, one_pair_array):
        x = np.zeros(shape=(1, Config.TIMESTEPS, Config.FINAL_SAMPLE_COLUMNS))
        y = np.zeros(shape=(1, 1))

        candle_counter = 0

        number_of_candles = np.shape(one_pair_array)[0]
        second_range = Config.TIMESTEPS
        first_range = math.floor(number_of_candles/second_range)
        second_range_expansion = number_of_candles - (first_range*second_range)

        for i in range(first_range - 1):    # -1 kvuli timesteps
            print(i)
            batch_array_1 = np.zeros(shape=(1, Config.TIMESTEPS, Config.FINAL_SAMPLE_COLUMNS))

            if i == first_range - 2:
                second_range += second_range_expansion
            for j in range(second_range):
                sample_3d, y_sample = self.sample_preprocessing(one_pair_array[candle_counter:candle_counter+Config.TIMESTEPS, :])
                y = np.concatenate((y, np.array([y_sample]).reshape(1, 1)), axis=0)
                batch_array_1 = np.concatenate((batch_array_1, sample_3d), axis=0)
                candle_counter += 1

            batch_array_1 = batch_array_1[1:, :, :]
            x = np.concatenate((x, batch_array_1), axis=0)

        x = x[1:, :, :]
        y = y[1:, :]

        return x, y

    def sample_preprocessing(self, sample_2d):
        sample_2d[:, 1:5] = self.normalize(sample_2d[:, 1:5])
        sample_2d[:, 5:6] = self.normalize(sample_2d[:, 5:6])     # rozsah 5:6 je furt jen sloupec 5, ale ma to 2d shape, ktery je potreba pro MinMaxScaler
        sample_2d[:, 6:7] = self.normalize(sample_2d[:, 6:7])
        sample_2d[:, 7:8] = self.normalize(sample_2d[:, 7:8])
        sample_2d[:, 8:9] = self.normalize(sample_2d[:, 8:9])
        sample_2d[:, 9:10] = self.normalize(sample_2d[:, 9:10])
        sample_2d[:, 10:12] = self.normalize(sample_2d[:, 10:12])
        sample_2d[:, 12:14] = self.normalize(sample_2d[:, 12:14])

        y = sample_2d[-1, 14]
        sample_2d = sample_2d[:, :-2]
        sample_3d = np.reshape(sample_2d, newshape=(1, np.shape(sample_2d)[0], np.shape(sample_2d)[1]))

        return sample_3d, y

    def normalize(self, array):
        scaler = MinMaxScaler()
        normalized_array = scaler.fit_transform(array)
        return normalized_array

    def normalize_time(self, dt):
        """0-24 hod do rozsahu 0-1"""
        normalized_time = float(dt.hour*3600+dt.minute*60+dt.second)/86400
        return normalized_time

    def create_samples_for_symbol(self):
        self.get_candles()
        one_pair_array = np.zeros(shape=(1, Config.NUMBER_OF_SAMPLE_COLUMNS))

        for i, candle in enumerate(self.candles):
            one_candle_array = np.zeros(shape=(1, Config.NUMBER_OF_SAMPLE_COLUMNS))

            one_candle_array[0, 0] = self.normalize_time(candle.open_time)
            one_candle_array[0, 1] = candle.open_price
            one_candle_array[0, 2] = candle.high_price
            one_candle_array[0, 3] = candle.low_price
            one_candle_array[0, 4] = candle.close_price
            one_candle_array[0, 5] = candle.volume
            one_candle_array[0, 6] = candle.quote_asset_volume
            one_candle_array[0, 7] = candle.number_of_trades
            one_candle_array[0, 8] = candle.taker_buy_base_asset_volume
            one_candle_array[0, 9] = candle.taker_buy_quote_asset_volume
            one_candle_array[0, 10] = candle.sma21
            one_candle_array[0, 11] = candle.sma200
            one_candle_array[0, 12] = candle.ema21
            one_candle_array[0, 13] = candle.ema200
            one_candle_array[0, 14] = candle.up
            one_candle_array[0, 15] = candle.down

            one_pair_array = np.concatenate((one_pair_array, one_candle_array), axis=0)
        one_pair_array = one_pair_array[1:, :]

        x, y = self.create3d_samples(one_pair_array)
        return self.create3d_samples(one_pair_array)



    @classmethod
    def get_sample_cls(cls, symbol):
        return Samples(symbol)

    @staticmethod
    def create_samples():
        for symbol in random.sample(Config.SYMBOLS_TO_SCRAPE, Config.RANDOM_SYMBOLS_FOR_SAMPLE):
            print(f"Creating samples from symbol={symbol}")

            samples = Samples.get_sample_cls(symbol)
            result_samples = samples.create_samples_for_symbol()
