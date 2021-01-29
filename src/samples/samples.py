from ..globals.config import Config
from ..data_analysis.models.views import ViewTypeWithRes, ViewWithtRes
from typing import List
import numpy as np
import pandas as pd
from sklearn.preprocessing import scale
import random
from collections import deque
from sklearn import preprocessing


def preprocess_df(df, shuffle=True):
    for col in df.columns:  # go through all of the columns
        if col != "target":  # normalize all ... except for the target itself!
            df[col] = df[col].pct_change()  # pct change "normalizes" the different currencies (each crypto coin has vastly diff values, we're really more interested in the other coin's movements)
            df.replace([np.inf, -np.inf], np.nan, inplace=True)
            df.dropna(inplace=True)  # remove the nas created by pct_change
            df[col] = preprocessing.scale(df[col].values)  # scale between 0 and 1.

    df.dropna(inplace=True)  # cleanup again... jic.

    sequential_data = []  # this is a list that will CONTAIN the sequences
    prev_days = deque(maxlen=Config.TIMESTEPS)  # These will be our actual sequences. They are made with deque, which keeps the maximum length by popping out older values as new ones come in

    for i in df.values:  # iterate over the values
        prev_days.append([n for n in i[:-1]])  # store all but the target
        if len(prev_days) == Config.TIMESTEPS:  # make sure we have 60 sequences!
            sequential_data.append([np.array(prev_days), i[-1]])  # append those bad boys!

    if shuffle:
        random.shuffle(sequential_data)  # shuffle for good measure.

        buys = []  # list that will store our buy sequences and targets
        sells = []  # list that will store our sell sequences and targets

        for seq, target in sequential_data:  # iterate over the sequential data
            if target == 0:  # if it's a "not buy"
                sells.append([seq, target])  # append to sells list
            elif target == 1:  # otherwise if the target is a 1...
                buys.append([seq, target])  # it's a buy!

        random.shuffle(buys)  # shuffle the buys
        random.shuffle(sells)  # shuffle the sells!

        lower = min(len(buys), len(sells))  # what's the shorter length?

        buys = buys[:lower]  # make sure both lists are only up to the shortest length.
        sells = sells[:lower]  # make sure both lists are only up to the shortest length.

        sequential_data = buys+sells  # add them together
        random.shuffle(sequential_data)  # another shuffle, so the model doesn't get confused with all 1 class then the other.

    X = []
    y = []

    for seq, target in sequential_data:  # going over our new sequential data
        X.append(seq)  # X is the sequences
        y.append(target)  # y is the targets/labels (buys vs sell/notbuy)

    return np.array(X), np.array(y)  # return X and y...and make X a numpy array!


class Samples:
    def __init__(self, candles: List[ViewTypeWithRes]):
        self.candles: List[ViewTypeWithRes] = candles
        self.candles: List[ViewTypeWithRes] = candles

    def __create3d_samples(self, features, results):
        if len(features) != len(results):
            raise Exception(f"Lenght of features {len(features)} does not match len of results {len(results)}")

        input_array = features[:]

        final_res = []
        batch_arrays = []

        for i in range(len(features)):
            # check overflow check
            if i + Config.TIMESTEPS >= len(input_array):
                break

            first_index = i
            second_index = i + Config.TIMESTEPS
            iter_res = results[second_index - 1]

            batch_array = input_array[first_index: second_index]
            batch_array = np.reshape(batch_array, (1, Config.TIMESTEPS, Config.FINAL_SAMPLE_COLUMNS))

            batch_array, add_enabled = self.__sample_preprocessing(batch_array, iter_res)

            if add_enabled:
                # Pokud add enable, vlozim krokovany sample a vysledek do listu, jinak zahodim
                batch_arrays.append(batch_array)
                # staci jen jeden result - protoze je to binarne - nahoru nebo dolu
                final_res.append(iter_res)

        # VStack az na konci -> v cyklu je nepouzitelny, protoze je extremne pomaly
        x = np.vstack([batch_arr for batch_arr in batch_arrays])
        x = np.reshape(scale(x[0], (1, Config.TIMESTEPS - 1, Config.FINAL_SAMPLE_COLUMNS)))

        y = np.array(final_res)
        return x, y

    def __sample_preprocessing(self, sample_2d, results):
        input_array = sample_2d[:]
        add_enable = True

        if ((results[0] == 0) and (results[1] == 0)) or np.any(np.isnan(input_array)) or np.any(np.isinf(input_array)):
            add_enable = False

        if add_enable:
            normalized_array = self.normalize(input_array)
        else:
            normalized_array = input_array

        return normalized_array, add_enable

    def normalize(self, array_2d):
        input_arr = array_2d[:][0]
        normalized_array = []

        for i, iter_arr in enumerate(input_arr):
            if i + 1 >= Config.TIMESTEPS:
                break

            next_arr = input_arr[i + 1]
            res_arr = ((next_arr - iter_arr) / iter_arr) * 100
            res_arr = np.nan_to_num(res_arr, nan=0, posinf=1, neginf=-1)
            normalized_array.append(res_arr)

        normalized_array = np.array(normalized_array)
        # normalized_array = np.vstack([arr for arr in np.array(normalized_array)])
        return np.reshape(normalized_array, (1, Config.TIMESTEPS - 1, Config.FINAL_SAMPLE_COLUMNS))

    def normalize_time(self, dt):
        """
        0-24 hod do rozsahu 0-1
        """
        normalized_time = float(dt.hour*3600+dt.minute*60+dt.second)/86400
        return normalized_time

    def create_samples_for_symbol(self, shuffle=True):
        df = pd.DataFrame([candle.get_as_dict() for candle in self.candles])

        x, y = preprocess_df(df, shuffle)
        return x, y

    @classmethod
    def get_sample_cls(cls, symbol):
        return Samples(symbol)

    @staticmethod
    def create_samples(candles, shuffle=True):
        samples = Samples(candles)
        return samples.create_samples_for_symbol(shuffle)

    @staticmethod
    def create_samples_for_symbols(symbols, start_date, end_date):
        print(f"Creating samples for symbol group {symbols} start={start_date} end_date={end_date}")
        train_candles = ViewWithtRes.get_train_candles(symbols, start_date, end_date)
        if len(train_candles) == 0:
            return []

        train_samples = Samples.create_samples(train_candles)
        print(f"Samples created")
        return train_samples

    @staticmethod
    def create_test_samples_for_symbols(symbols, start_date, end_date):
        print(f"Creating test samples for symbol group {symbols} start_date={start_date} end_date={end_date}")
        test_candles = ViewWithtRes.get_test_candles_for_symbols(symbols, start_date, end_date)
        if len(test_candles) == 0:
            return []
        test_candles = Samples.create_samples(test_candles)
        print(f"Test samples created")
        return test_candles
