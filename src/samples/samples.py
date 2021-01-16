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
        
        add_enable = True
        normalized_array[:, 1:5] = self.normalize(input_array[:, 1:5])

        if not np.isnan(input_array).any():
            for i in range(5, np.shape(input_array)[1] - 2):
                normalized_array[:, i] = self.normalize(input_array[:, i])
        else:
            add_enable = False
        
        if (input_array[-1, 90] == 0) and (input_array[-1, 91] == 0):
            add_enable = False

        y = input_array[-1, 90]
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

            one_candle_array[0, 10] = candle.momentum_ao
            one_candle_array[0, 11] = candle.momentum_kama
            one_candle_array[0, 12] = candle.momentum_ppo
            one_candle_array[0, 13] = candle.momentum_ppo_hist
            one_candle_array[0, 14] = candle.momentum_ppo_signal
            one_candle_array[0, 15] = candle.momentum_roc
            one_candle_array[0, 16] = candle.momentum_tsi
            one_candle_array[0, 17] = candle.momentum_uo
            one_candle_array[0, 18] = candle.momentum_wr
            one_candle_array[0, 19] = candle.momentum_rsi
            one_candle_array[0, 20] = candle.momentum_stoch_rsi
            one_candle_array[0, 21] = candle.momentum_stoch_rsi_d
            one_candle_array[0, 22] = candle.momentum_stoch_rsi_k
            one_candle_array[0, 23] = candle.momentum_stoch_signal

            one_candle_array[0, 24] = candle.trend_adx
            one_candle_array[0, 25] = candle.trend_adx_neg
            one_candle_array[0, 26] = candle.trend_adx_pos
            one_candle_array[0, 27] = candle.trend_aroon_down
            one_candle_array[0, 28] = candle.trend_aroon_up
            one_candle_array[0, 29] = candle.trend_aroon_ind
            one_candle_array[0, 30] = candle.trend_psar_down
            one_candle_array[0, 31] = candle.trend_psar_up
            one_candle_array[0, 32] = candle.trend_psar_down_indicator
            one_candle_array[0, 33] = candle.trend_macd
            one_candle_array[0, 34] = candle.trend_macd_diff
            one_candle_array[0, 35] = candle.trend_macd_signal
            one_candle_array[0, 36] = candle.trend_cci
            one_candle_array[0, 37] = candle.trend_stc
            one_candle_array[0, 38] = candle.trend_trix
            one_candle_array[0, 39] = candle.trend_kst
            one_candle_array[0, 40] = candle.trend_kst_diff
            one_candle_array[0, 41] = candle.trend_kst_sig
            one_candle_array[0, 42] = candle.trend_ema_fast
            one_candle_array[0, 43] = candle.trend_ema_slow
            one_candle_array[0, 44] = candle.trend_sma_fast
            one_candle_array[0, 45] = candle.trend_sma_slow
            one_candle_array[0, 46] = candle.trend_ichimoku_a
            one_candle_array[0, 47] = candle.trend_ichimoku_b
            one_candle_array[0, 48] = candle.trend_ichimoku_base
            one_candle_array[0, 49] = candle.trend_ichimoku_conv
            one_candle_array[0, 50] = candle.trend_visual_ichimoku_a
            one_candle_array[0, 51] = candle.trend_visual_ichimoku_b
            one_candle_array[0, 52] = candle.trend_vortex_ind_pos
            one_candle_array[0, 53] = candle.trend_vortex_ind_diff
            one_candle_array[0, 54] = candle.trend_vortex_ind_pos
            one_candle_array[0, 55] = candle.trend_vortex_ind_neg

            one_candle_array[0, 56] = candle.others_cr
            one_candle_array[0, 57] = candle.others_dr
            one_candle_array[0, 58] = candle.others_dlr
            
            one_candle_array[0, 59] = candle.volume_adi
            one_candle_array[0, 60] = candle.volume_cmf
            one_candle_array[0, 61] = candle.volume_em
            one_candle_array[0, 62] = candle.volume_fi
            one_candle_array[0, 63] = candle.volume_mfi
            one_candle_array[0, 64] = candle.volume_nvi
            one_candle_array[0, 65] = candle.volume_obv
            one_candle_array[0, 66] = candle.volume_sma_em
            one_candle_array[0, 67] = candle.volume_vpt
            one_candle_array[0, 68] = candle.volume_vwap

            one_candle_array[0, 69] = candle.volatility_atr
            one_candle_array[0, 70] = candle.volatility_bbh
            one_candle_array[0, 71] = candle.volatility_bbhi
            one_candle_array[0, 72] = candle.volatility_bbl
            one_candle_array[0, 73] = candle.volatility_bbli
            one_candle_array[0, 74] = candle.volatility_bbm
            one_candle_array[0, 75] = candle.volatility_bbp
            one_candle_array[0, 76] = candle.volatility_bbw
            one_candle_array[0, 77] = candle.volatility_dch
            one_candle_array[0, 78] = candle.volatility_dcl
            one_candle_array[0, 79] = candle.volatility_dcm
            one_candle_array[0, 80] = candle.volatility_dcp
            one_candle_array[0, 81] = candle.volatility_dcw
            one_candle_array[0, 82] = candle.volatility_kcc
            one_candle_array[0, 83] = candle.volatility_kch
            one_candle_array[0, 84] = candle.volatility_kchi
            one_candle_array[0, 85] = candle.volatility_kcl
            one_candle_array[0, 86] = candle.volatility_kcp
            one_candle_array[0, 87] = candle.volatility_kcli
            one_candle_array[0, 88] = candle.volatility_kcw
            one_candle_array[0, 89] = candle.volatility_ui

            one_candle_array[0, 90] = candle.up
            one_candle_array[0, 91] = candle.down

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
