from ...globals.db import DB
from sqlalchemy import Table, Column, Integer, asc, and_, or_
from typing import List


db = DB.get_globals()


class ViewTypeWithoutRes:
    id = None
    symbol = None
    open_time = None
    open_price = None
    high_price = None
    low_price = None
    close_price = None
    volume = None
    close_time = None
    quote_asset_volume = None
    number_of_trades = None
    taker_buy_base_asset_volume = None
    taker_buy_quote_asset_volume = None

    volume_adi = None
    volume_obv = None
    volume_cmf = None
    volume_fi = None
    volume_mfi = None
    volume_em = None
    volume_sma_em = None
    volume_vpt = None
    volume_nvi = None
    volume_vwap = None

    volatility_atr = None
    volatility_bbm = None
    volatility_bbh = None
    volatility_bbl = None
    volatility_bbw = None
    volatility_bbp = None
    volatility_bbhi = None
    volatility_bbli = None
    volatility_kcc = None
    volatility_kch = None
    volatility_kcl = None
    volatility_kcw = None
    volatility_kcp = None
    volatility_kchi = None
    volatility_kcli = None
    volatility_dcl = None
    volatility_dch = None
    volatility_dcm = None
    volatility_dcw = None
    volatility_dcp = None
    volatility_ui = None

    trend_macd = None
    trend_macd_signal = None
    trend_macd_diff = None
    trend_sma_fast = None
    trend_sma_slow = None
    trend_ema_fast = None
    trend_ema_slow = None
    trend_adx = None
    trend_adx_pos = None
    trend_adx_neg = None
    trend_vortex_ind_pos = None
    trend_vortex_ind_neg = None
    trend_vortex_ind_diff = None
    trend_trix = None
    trend_mass_index = None
    trend_cci = None
    trend_dpo = None
    trend_kst = None
    trend_kst_sig = None
    trend_kst_diff = None
    trend_ichimoku_conv = None
    trend_ichimoku_base = None
    trend_ichimoku_a = None
    trend_ichimoku_b = None
    trend_visual_ichimoku_a = None
    trend_visual_ichimoku_b = None
    trend_aroon_up = None
    trend_aroon_down = None
    trend_aroon_ind = None
    trend_psar_up = None
    trend_psar_down = None
    trend_psar_up_indicator = None
    trend_psar_down_indicator = None
    trend_stc = None

    momentum_rsi = None
    momentum_stoch_rsi = None
    momentum_stoch_rsi_k = None
    momentum_stoch_rsi_d = None
    momentum_tsi = None
    momentum_uo = None
    momentum_stoch = None
    momentum_stoch_signal = None
    momentum_wr = None
    momentum_ao = None
    momentum_kama = None
    momentum_roc = None
    momentum_ppo = None
    momentum_ppo_signal = None
    momentum_ppo_hist = None

    others_dr = None
    others_dlr = None
    others_cr = None


class ViewTypeWithRes(ViewTypeWithoutRes):
    up = None
    down = None
    train = None


class ViewWithtRes(ViewTypeWithRes, db.DECLARATIVE_BASE):
    __table__ = Table("VJoinedVRes", db.DECLARATIVE_BASE.metadata,
                        Column("id", Integer, primary_key=True),
                        autoload=True, autoload_with=db.ENGINE,
                    )

    @staticmethod
    def get_test_candles() -> List[ViewTypeWithRes]:
        test_candles = db.SESSION.query(ViewWithtRes).filter(ViewWithtRes.train == False).order_by(asc(ViewWithtRes.open_time)).all()
        return test_candles

    @classmethod
    def get_test_candles_for_symbols(cls, symbols) -> List[ViewTypeWithRes]:
        train_expression = getattr(cls, "train") == False

        return db.SESSION.query(ViewWithtRes).filter(and_(train_expression, ViewWithtRes.symbol.in_(symbols))).order_by(
            asc(ViewWithtRes.open_time)).all()

    @staticmethod
    def get_train_candles_for_symbol(symbol) -> List[ViewTypeWithRes]:
        train_candles = db.SESSION.query(ViewWithtRes).filter(
            and_(ViewWithtRes.symbol == symbol, ViewWithtRes.train == True)).order_by(
            asc(ViewWithtRes.open_time)).all()
        return train_candles

    @classmethod
    def get_train_candles(cls, symbols: List[str]):
        train_expression = getattr(cls, "train") == True
        return db.SESSION.query(ViewWithtRes).filter(and_(train_expression, ViewWithtRes.symbol.in_(symbols))).order_by(
            asc(ViewWithtRes.open_time)).all()

    def __repr__(self):
        return f"symbol={self.symbol} open_time={self.open_time} up={self.up} down={self.down}"


"""
Priklad pouziti.. dulezite je pridat typ List[ViewTypeWithRes] potom to bude radit typy
def test(*args):
    res: List[ViewTypeWithRes] = DB.SESSION.query(ViewWithtRes)
    for r in res:
        print(r.symbol)
"""
