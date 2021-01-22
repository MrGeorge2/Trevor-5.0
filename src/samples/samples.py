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
        # otocim si i vysledky - abych to mel ve stejnym shapu

        for i in range(len(features)):
            # check overflow check
            if i + Config.TIMESTEPS >= len(input_array):
                break

            first_index = i
            second_index = i + Config.TIMESTEPS
            iter_res = results[i]

            batch_array = input_array[first_index: second_index]
            batch_array = np.reshape(batch_array, (1, Config.TIMESTEPS, Config.FINAL_SAMPLE_COLUMNS))

            batch_array, add_enabled = self.__sample_preprocessing(batch_array, iter_res)

            if add_enabled:
                # Pokud add enable, vlozim krokovany sample a vysledek do listu, jinak zahodim
                batch_array = np.reshape(batch_array, (1, Config.TIMESTEPS, Config.FINAL_SAMPLE_COLUMNS))
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
        input_arr = array_2d[:]

        scaler = StandardScaler(with_mean=0, with_std=1)
        scaler.fit(input_arr[0])
        normalized_array = scaler.transform(X=input_arr[0])
        return normalized_array

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
        y = np.array(one_pair_results)

        x = self.__create3d_samples(np_one_pair_features[:], y[:])
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
