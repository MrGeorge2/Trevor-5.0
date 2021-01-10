from ..globals.config import Config
from ..data_analysis.models.views import ViewTypeWithRes, ViewWithtRes
from typing import List
import numpy as np
import math
from copy import deepcopy


class Samples:
    def __init__(self, candles: List[ViewTypeWithRes]):
        self.candles: List[ViewTypeWithRes] = candles

    def create3d_samples(self, one_pair_array):
        input_array = deepcopy(one_pair_array)
        x = np.zeros(shape=(1, Config.TIMESTEPS, Config.FINAL_SAMPLE_COLUMNS))
        y = np.zeros(shape=(1, 1))

        candle_counter = 0

        number_of_candles = np.shape(one_pair_array)[0]
        second_range = Config.TIMESTEPS
        first_range = math.floor(number_of_candles/second_range)
        second_range_expansion = number_of_candles - (first_range*second_range)

        for i in range(first_range - 1):    # -1 kvuli timesteps
            batch_array_1 = np.zeros(shape=(1, Config.TIMESTEPS, Config.FINAL_SAMPLE_COLUMNS))

            if i == first_range - 2:
                second_range += second_range_expansion
            for j in range(second_range):
                normalized_array, y_sample, add_enable = self.sample_preprocessing(input_array[candle_counter:candle_counter+Config.TIMESTEPS, :])
                if add_enable:
                    normalized_array = np.reshape(normalized_array, newshape=(1, Config.TIMESTEPS, Config.FINAL_SAMPLE_COLUMNS))
                    y = np.concatenate((y, np.array([y_sample]).reshape(1, 1)), axis=0)
                    batch_array_1 = np.concatenate((batch_array_1, normalized_array), axis=0)
                candle_counter += 1

            batch_array_1 = batch_array_1[1:, :, :]
            x = np.concatenate((x, batch_array_1), axis=0)

        x = x[1:, :, :]
        y = y[1:, :]

        return x, y

    def sample_preprocessing(self, sample_2d):
        input_array = deepcopy(sample_2d)
        normalized_array = deepcopy(sample_2d)
        normalized_array[:, 1:5] = self.normalize(input_array[:, 1:5])
        normalized_array[:, 5] = self.normalize(input_array[:, 5])     # rozsah 5:6 je furt jen sloupec 5, ale ma to 2d shape, ktery je potreba pro MinMaxScaler
        normalized_array[:, 6] = self.normalize(input_array[:, 6])
        normalized_array[:, 7] = self.normalize(input_array[:, 7])
        normalized_array[:, 8] = self.normalize(input_array[:, 8])
        normalized_array[:, 9] = self.normalize(input_array[:, 9])
        normalized_array[:, 10:12] = self.normalize(input_array[:, 10:12])
        normalized_array[:, 12:14] = self.normalize(input_array[:, 12:14])

        add_enable = True
        if (input_array[-1, 14] == 0) and (input_array[-1, 15] == 0):
            add_enable = False

        y = input_array[-1, 14]
        normalized_array = normalized_array[:, :-2]
        # sample_3d = np.reshape(normalized_array, newshape=(1, np.shape(sample_2d)[0], np.shape(sample_2d)[1]))
        return normalized_array, y, add_enable

    def normalize(self, array_2d):
        """
        scaler = MinMaxScaler()
        normalized_array = scaler.fit_transform(array)
        """
        minumum = array_2d.min()
        maximum = array_2d.max()
        normalized_array = (array_2d - minumum) / (maximum - minumum)
        return normalized_array

    def normalize_time(self, dt):
        """
        0-24 hod do rozsahu 0-1
        """
        normalized_time = float(dt.hour*3600+dt.minute*60+dt.second)/86400
        return normalized_time

    def create_samples_for_symbol(self):
        # self.get_candles()
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

            one_pair_array = np.concatenate((one_pair_array, one_candle_array), axis=0).astype(np.float32)
        one_pair_array = one_pair_array[1:, :]
        o_p_a = deepcopy(one_pair_array)

        x, y = self.create3d_samples(o_p_a)
        return x, y

    @classmethod
    def get_sample_cls(cls, symbol):
        return Samples(symbol)

    @staticmethod
    def create_samples(candles):
        samples = Samples(candles)
        return samples.create_samples_for_symbol()

    @staticmethod
    def create_samples_for_symbols(symbols):
        print(f"Creating samples for symbol group {symbols}")
        train_candles = ViewWithtRes.get_train_candles(symbols)
        train_samples = Samples.create_samples(train_candles)
        print(f"Samples created")
        return train_samples
