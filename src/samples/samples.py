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

        if np.isnan(input_array).any():
            add_enable = False
        else:
            for i in range(5, np.shape(input_array)[1] - 2):
                normalized_array[:, i] = self.normalize(input_array[:, i])
        
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

            one_candle_array[0, 0] = None if self.normalize_time(candle.open_time) is None else float(self.normalize_time(candle.open_time))
            one_candle_array[0, 1] = None if candle.open_price is None else float(candle.open_price)
            one_candle_array[0, 2] = None if candle.high_price is None else float(candle.high_price)
            one_candle_array[0, 3] = None if candle.low_price is None else float(candle.low_price)
            one_candle_array[0, 4] = None if candle.close_price is None else float(candle.close_price)
            one_candle_array[0, 5] = None if candle.volume is None else float(candle.volume)
            one_candle_array[0, 6] = None if candle.quote_asset_volume is None else float(candle.quote_asset_volume)
            one_candle_array[0, 7] = None if candle.number_of_trades is None else float(candle.number_of_trades)
            one_candle_array[0, 8] = None if candle.taker_buy_base_asset_volume is None else float(candle.taker_buy_base_asset_volume)
            one_candle_array[0, 9] = None if candle.taker_buy_quote_asset_volume is None else float(candle.taker_buy_quote_asset_volume)

            one_candle_array[0, 10] = None if candle.momentum_ao is None else float(candle.momentum_ao)
            one_candle_array[0, 11] = None if candle.momentum_kama is None else float(candle.momentum_kama)
            one_candle_array[0, 12] = None if candle.momentum_ppo is None else float(candle.momentum_ppo)
            one_candle_array[0, 13] = None if candle.momentum_ppo_hist is None else float(candle.momentum_ppo_hist)
            one_candle_array[0, 14] = None if candle.momentum_ppo_signal is None else float(candle.momentum_ppo_signal)
            one_candle_array[0, 15] = None if candle.momentum_roc is None else float(candle.momentum_roc)
            one_candle_array[0, 16] = None if candle.momentum_tsi is None else float(candle.momentum_tsi)
            one_candle_array[0, 17] = None if candle.momentum_uo is None else float(candle.momentum_uo)
            one_candle_array[0, 18] = None if candle.momentum_wr is None else float(candle.momentum_wr)
            one_candle_array[0, 19] = None if candle.momentum_rsi is None else float(candle.momentum_rsi)
            one_candle_array[0, 20] = None if candle.momentum_stoch_rsi is None else float(candle.momentum_stoch_rsi)
            one_candle_array[0, 21] = None if candle.momentum_stoch_rsi_d is None else float(candle.momentum_stoch_rsi_d)
            one_candle_array[0, 22] = None if candle.momentum_stoch_rsi_k is None else float(candle.momentum_stoch_rsi_k)
            one_candle_array[0, 23] = None if candle.momentum_stoch_signal is None else float(candle.momentum_stoch_signal)

            one_candle_array[0, 24] = None if candle.trend_adx is None else float(candle.trend_adx)
            one_candle_array[0, 25] = None if candle.trend_adx_neg is None else float(candle.trend_adx_neg)
            one_candle_array[0, 26] = None if candle.trend_adx_pos is None else float(candle.trend_adx_pos)
            one_candle_array[0, 27] = None if candle.trend_aroon_down is None else float(candle.trend_aroon_down)
            one_candle_array[0, 28] = None if candle.trend_aroon_up is None else float(candle.trend_aroon_up)
            one_candle_array[0, 29] = None if candle.trend_aroon_ind is None else float(candle.trend_aroon_ind)
            one_candle_array[0, 30] = None if candle.trend_psar_down is None else float(candle.trend_psar_down)
            one_candle_array[0, 31] = None if candle.trend_psar_up is None else float(candle.trend_psar_up)
            one_candle_array[0, 32] = None if candle.trend_psar_down_indicator is None else float(candle.trend_psar_down_indicator)
            one_candle_array[0, 33] = None if candle.trend_macd is None else float(candle.trend_macd)
            one_candle_array[0, 34] = None if candle.trend_macd_diff is None else float(candle.trend_macd_diff)
            one_candle_array[0, 35] = None if candle.trend_macd_signal is None else float(candle.trend_macd_signal)
            one_candle_array[0, 36] = None if candle.trend_cci is None else float(candle.trend_cci)
            one_candle_array[0, 37] = None if candle.trend_stc is None else float(candle.trend_stc)
            one_candle_array[0, 38] = None if candle.trend_trix is None else float(candle.trend_trix)
            one_candle_array[0, 39] = None if candle.trend_kst is None else float(candle.trend_kst)
            one_candle_array[0, 40] = None if candle.trend_kst_diff is None else float(candle.trend_kst_diff)
            one_candle_array[0, 41] = None if candle.trend_kst_sig is None else float(candle.trend_kst_sig)
            one_candle_array[0, 42] = None if candle.trend_ema_fast is None else float(candle.trend_ema_fast)
            one_candle_array[0, 43] = None if candle.trend_ema_slow is None else float(candle.trend_ema_slow)
            one_candle_array[0, 44] = None if candle.trend_sma_fast is None else float(candle.trend_sma_fast)
            one_candle_array[0, 45] = None if candle.trend_sma_slow is None else float(candle.trend_sma_slow)
            one_candle_array[0, 46] = None if candle.trend_ichimoku_a is None else float(candle.trend_ichimoku_a)
            one_candle_array[0, 47] = None if candle.trend_ichimoku_b is None else float(candle.trend_ichimoku_b)
            one_candle_array[0, 48] = None if candle.trend_ichimoku_base is None else float(candle.trend_ichimoku_base)
            one_candle_array[0, 49] = None if candle.trend_ichimoku_conv is None else float(candle.trend_ichimoku_conv)
            one_candle_array[0, 50] = None if candle.trend_visual_ichimoku_a is None else float(candle.trend_visual_ichimoku_a)
            one_candle_array[0, 51] = None if candle.trend_visual_ichimoku_b is None else float(candle.trend_visual_ichimoku_b)
            one_candle_array[0, 52] = None if candle.trend_vortex_ind_pos is None else float(candle.trend_vortex_ind_pos)
            one_candle_array[0, 53] = None if candle.trend_vortex_ind_diff is None else float(candle.trend_vortex_ind_diff)
            one_candle_array[0, 54] = None if candle.trend_vortex_ind_pos is None else float(candle.trend_vortex_ind_pos)
            one_candle_array[0, 55] = None if candle.trend_vortex_ind_neg is None else float(candle.trend_vortex_ind_neg)

            one_candle_array[0, 56] = None if candle.others_cr is None else float(candle.others_cr)
            one_candle_array[0, 57] = None if candle.others_dr is None else float(candle.others_dr)
            one_candle_array[0, 58] = None if candle.others_dlr is None else float(candle.others_dlr)
            
            one_candle_array[0, 59] = None if candle.volume_adi is None else float(candle.volume_adi)
            one_candle_array[0, 60] = None if candle.volume_cmf is None else float(candle.volume_cmf)
            one_candle_array[0, 61] = None if candle.volume_em is None else float(candle.volume_em)
            one_candle_array[0, 62] = None if candle.volume_fi is None else float(candle.volume_fi)
            one_candle_array[0, 63] = None if candle.volume_mfi is None else float(candle.volume_mfi)
            one_candle_array[0, 64] = None if candle.volume_nvi is None else float(candle.volume_nvi)
            one_candle_array[0, 65] = None if candle.volume_obv is None else float(candle.volume_obv)
            one_candle_array[0, 66] = None if candle.volume_sma_em is None else float(candle.volume_sma_em)
            one_candle_array[0, 67] = None if candle.volume_vpt is None else float(candle.volume_vpt)
            one_candle_array[0, 68] = None if candle.volume_vwap is None else float(candle.volume_vwap)

            one_candle_array[0, 69] = None if candle.volatility_atr is None else float(candle.volatility_atr)
            one_candle_array[0, 70] = None if candle.volatility_bbh is None else float(candle.volatility_bbh)
            one_candle_array[0, 71] = None if candle.volatility_bbhi is None else float(candle.volatility_bbhi)
            one_candle_array[0, 72] = None if candle.volatility_bbl is None else float(candle.volatility_bbl)
            one_candle_array[0, 73] = None if candle.volatility_bbli is None else float(candle.volatility_bbli)
            one_candle_array[0, 74] = None if candle.volatility_bbm is None else float(candle.volatility_bbm)
            one_candle_array[0, 75] = None if candle.volatility_bbp is None else float(candle.volatility_bbp)
            one_candle_array[0, 76] = None if candle.volatility_bbw is None else float(candle.volatility_bbw)
            one_candle_array[0, 77] = None if candle.volatility_dch is None else float(candle.volatility_dch)
            one_candle_array[0, 78] = None if candle.volatility_dcl is None else float(candle.volatility_dcl)
            one_candle_array[0, 79] = None if candle.volatility_dcm is None else float(candle.volatility_dcm)
            one_candle_array[0, 80] = None if candle.volatility_dcp is None else float(candle.volatility_dcp)
            one_candle_array[0, 81] = None if candle.volatility_dcw is None else float(candle.volatility_dcw)
            one_candle_array[0, 82] = None if candle.volatility_kcc is None else float(candle.volatility_kcc)
            one_candle_array[0, 83] = None if candle.volatility_kch is None else float(candle.volatility_kch)
            one_candle_array[0, 84] = None if candle.volatility_kchi is None else float(candle.volatility_kchi)
            one_candle_array[0, 85] = None if candle.volatility_kcl is None else float(candle.volatility_kcl)
            one_candle_array[0, 86] = None if candle.volatility_kcp is None else float(candle.volatility_kcp)
            one_candle_array[0, 87] = None if candle.volatility_kcli is None else float(candle.volatility_kcli)
            one_candle_array[0, 88] = None if candle.volatility_kcw is None else float(candle.volatility_kcw)
            one_candle_array[0, 89] = None if candle.volatility_ui is None else float(candle.volatility_ui)

            one_candle_array[0, 90] = None if candle.up is None else float(candle.up)
            one_candle_array[0, 91] = None if candle.down is None else float(candle.down)

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
