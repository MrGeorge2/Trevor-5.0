from ...globals.db import DB
from .candle_api import CandleApi
from ...globals.config import Config
from sqlalchemy import Column, DECIMAL, DATETIME, Integer, String, ForeignKey, and_, asc
from typing import List
from decimal import Decimal
import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna


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
            cols = df.columns
            for i in range(len(cols)):
                print(cols[i])
            input()
            pass
            """
            print(f"Counting indentificators for {symbol}")
            sum21 = 0
            sum21count = 0

            sum200 = 0
            sum200count = 0

            candles: List[CandleApi] = db.SESSION.query(CandleApi).filter(
                CandleApi.symbol == symbol).order_by(asc(CandleApi.open_time)).all()

            for i, candle in enumerate(candles):
                sum21 += candle.close_price
                sum21count += 1

                sum200 += candle.close_price
                sum200count += 1

                if i > 200:
                    if Config.CHECK_ROW_IN_DB:
                        if not db.SESSION.query(db.SESSION.query(Indicators).filter(
                                and_(Indicators.symbol == candle.symbol,
                                     Indicators.open_time == candle.open_time)).exists()).scalar():
                            ind = Indicators(
                                    sma21=sum21/21,
                                    sma200=sum200/200,
                                    ema21=Indicators.count_ema(candle, Decimal(sum21/21), 21),
                                    ema200=Indicators.count_ema(candle, Decimal(sum200/200), 200),
                                    open_time=candle.open_time,
                                    symbol=candle.symbol)
                            db.SESSION.add(ind)
                    else:
                        ind = Indicators(
                            sma21=sum21 / 21,
                            sma200=sum200 / 200,
                            ema21=Indicators.count_ema(candle, Decimal(sum21 / 21), 21),
                            ema200=Indicators.count_ema(candle, Decimal(sum200 / 200), 200),
                            open_time=candle.open_time,
                            symbol=candle.symbol)
                        db.SESSION.add(ind)

                if sum21count >= 21:
                    sum21count -= 1
                    sum21 -= candles[i-20].close_price

                if sum200count >= 200:
                    sum200count -= 1
                    sum200 -= candles[i-199].close_price

            db.SESSION.commit()
            print(f"Done")

"""