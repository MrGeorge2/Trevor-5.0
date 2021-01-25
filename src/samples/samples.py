from ..globals.config import Config
from ..data_analysis.models.views import ViewTypeWithRes, ViewWithtRes
from typing import List
import numpy as np
from sklearn.preprocessing import StandardScaler


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
                final_res.append(iter_res[0])

        # VStack az na konci -> v cyklu je nepouzitelny, protoze je extremne pomaly
        x = np.vstack([batch_arr for batch_arr in batch_arrays])
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
        """
        scaler = StandardScaler(with_mean=0, with_std=1)
        # beru nulty index protoze je shape (1, timesteps, features)
        scaler.fit(input_arr[0])
        normalized_array = scaler.transform(X=input_arr[0])
        """
        normalized_array = np.array(normalized_array)
        # normalized_array = np.vstack([arr for arr in np.array(normalized_array)])
        return np.reshape(normalized_array, (1, Config.TIMESTEPS - 1, Config.FINAL_SAMPLE_COLUMNS))

    def normalize_time(self, dt):
        """
        0-24 hod do rozsahu 0-1
        """
        normalized_time = float(dt.hour*3600+dt.minute*60+dt.second)/86400
        return normalized_time

    def create_samples_for_symbol(self):
        one_pair_features = []
        one_pair_results = []

        for i, candle in enumerate(self.candles):
            features = candle.get_features()
            results = candle.get_results()

            one_pair_features.append(features)
            one_pair_results.append(results)

        np_one_pair_features = np.array(one_pair_features)
        np_one_pair_results = np.array(one_pair_results)

        x, y = self.__create3d_samples(np_one_pair_features[:], np_one_pair_results[:])
        return x, y

    @classmethod
    def get_sample_cls(cls, symbol):
        return Samples(symbol)

    @staticmethod
    def create_samples(candles):
        samples = Samples(candles)
        return samples.create_samples_for_symbol()

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
