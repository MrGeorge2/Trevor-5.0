from ...globals.db import DB
from .candle_api import CandleApi
from ...globals.config import Config
from sqlalchemy import Column, DECIMAL, DATETIME, Integer, String, ForeignKey, and_, asc
from typing import List
import pandas as pd
from ta import add_all_ta_features


class Indicators(DB.DECLARATIVE_BASE):
    __tablename__ = "TIndicators"
    id = Column(Integer, primary_key=True)
    open_time = Column(DATETIME, ForeignKey(CandleApi.open_time))
    symbol = Column(String, ForeignKey(CandleApi.symbol))

    volume_adi = Column(DECIMAL)
    volume_obv = Column(DECIMAL)
    volume_cmf = Column(DECIMAL)
    volume_fi = Column(DECIMAL)
    volume_mfi = Column(DECIMAL)
    volume_em = Column(DECIMAL)
    volume_sma_em = Column(DECIMAL)
    volume_vpt = Column(DECIMAL)
    volume_nvi = Column(DECIMAL)
    volume_vwap = Column(DECIMAL)

    volatility_atr = Column(DECIMAL)
    volatility_bbm = Column(DECIMAL)
    volatility_bbh = Column(DECIMAL)
    volatility_bbl = Column(DECIMAL)
    volatility_bbw = Column(DECIMAL)
    volatility_bbp = Column(DECIMAL)
    volatility_bbhi = Column(DECIMAL)
    volatility_bbli = Column(DECIMAL)
    volatility_kcc = Column(DECIMAL)
    volatility_kch = Column(DECIMAL)
    volatility_kcl = Column(DECIMAL)
    volatility_kcw = Column(DECIMAL)
    volatility_kcp = Column(DECIMAL)
    volatility_kchi = Column(DECIMAL)
    volatility_kcli = Column(DECIMAL)
    volatility_dcl = Column(DECIMAL)
    volatility_dch = Column(DECIMAL)
    volatility_dcm = Column(DECIMAL)
    volatility_dcw = Column(DECIMAL)
    volatility_dcp = Column(DECIMAL)
    volatility_ui = Column(DECIMAL)

    trend_macd = Column(DECIMAL)
    trend_macd_signal = Column(DECIMAL)
    trend_macd_diff = Column(DECIMAL)
    trend_sma_fast = Column(DECIMAL)
    trend_sma_slow = Column(DECIMAL)
    trend_ema_fast = Column(DECIMAL)
    trend_ema_slow = Column(DECIMAL)
    trend_adx = Column(DECIMAL)
    trend_adx_pos = Column(DECIMAL)
    trend_adx_neg = Column(DECIMAL)
    trend_vortex_ind_pos = Column(DECIMAL)
    trend_vortex_ind_neg = Column(DECIMAL)
    trend_vortex_ind_diff = Column(DECIMAL)
    trend_trix = Column(DECIMAL)
    trend_mass_index = Column(DECIMAL)
    trend_cci = Column(DECIMAL)
    trend_dpo = Column(DECIMAL)
    trend_kst = Column(DECIMAL)
    trend_kst_sig = Column(DECIMAL)
    trend_kst_diff = Column(DECIMAL)
    trend_ichimoku_conv = Column(DECIMAL)
    trend_ichimoku_base = Column(DECIMAL)
    trend_ichimoku_a = Column(DECIMAL)
    trend_ichimoku_b = Column(DECIMAL)
    trend_visual_ichimoku_a = Column(DECIMAL)
    trend_visual_ichimoku_b = Column(DECIMAL)
    trend_aroon_up = Column(DECIMAL)
    trend_aroon_down = Column(DECIMAL)
    trend_aroon_ind = Column(DECIMAL)
    trend_psar_up = Column(DECIMAL)
    trend_psar_down = Column(DECIMAL)
    trend_psar_up_indicator = Column(DECIMAL)
    trend_psar_down_indicator = Column(DECIMAL)
    trend_stc = Column(DECIMAL)

    momentum_rsi = Column(DECIMAL)
    momentum_stoch_rsi = Column(DECIMAL)
    momentum_stoch_rsi_k = Column(DECIMAL)
    momentum_stoch_rsi_d = Column(DECIMAL)
    momentum_tsi = Column(DECIMAL)
    momentum_uo = Column(DECIMAL)
    momentum_stoch = Column(DECIMAL)
    momentum_stoch_signal = Column(DECIMAL)
    momentum_wr = Column(DECIMAL)
    momentum_ao = Column(DECIMAL)
    momentum_kama = Column(DECIMAL)
    momentum_roc = Column(DECIMAL)
    momentum_ppo = Column(DECIMAL)
    momentum_ppo_signal = Column(DECIMAL)
    momentum_ppo_hist = Column(DECIMAL)

    others_dr = Column(DECIMAL)
    others_dlr = Column(DECIMAL)
    others_cr = Column(DECIMAL)

    @staticmethod
    def count_indicators(*args):
        db = DB.get_globals()

        for symbol in Config.SYMBOLS_TO_SCRAPE:
            print(f"Counting indentificators for {symbol}")
            candles: List[CandleApi] = db.SESSION.query(CandleApi).filter(
                CandleApi.symbol == symbol).order_by(asc(CandleApi.open_time)).all()
            df = pd.DataFrame([candle.prices_as_dict() for candle in candles])
            df = add_all_ta_features(
                df,
                open="open_time",
                high="high_price",
                low="low_price",
                close="close_price",
                volume="volume",
            )

            # remove cols that are not in TIndicators
            df = df.drop(
                [
                    'open_price',
                    'high_price',
                    'low_price',
                    'close_price',
                    'volume',
                ],
                axis='columns')

            df['trend_psar_up'] = df['trend_psar_up'].fillna(0)
            df['trend_psar_down'] = df['trend_psar_down'].fillna(0)

            for i, data in df.iterrows():
                if Config.CHECK_ROW_IN_DB:

                    if not db.SESSION.query(db.SESSION.query(Indicators).filter(
                            and_(Indicators.symbol == symbol,
                                 Indicators.open_time == data["open_time"])).exists()).scalar():
                        ind = Indicators(**data)
                        db.SESSION.add(ind)
                else:
                    ind = Indicators(**data)
                    ind.symbol = symbol
                    db.SESSION.add(ind)
            db.SESSION.commit()
            print(f"Done")
