from ...globals.DB import DB
from sqlalchemy import Table, Column, Integer, asc, and_, or_
from typing import List


DB = DB.get_globals()


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
    sma21 = None
    sma200 = None
    ema21 = None
    ema200 = None


class ViewWithoutRes(ViewTypeWithoutRes, DB.DECLARATIVE_BASE):
    __table__ = Table("VJoined", DB.DECLARATIVE_BASE.metadata,
                      Column("id", Integer, primary_key=True),
                             autoload=True, autoload_with=DB.ENGINE
                    )


class ViewTypeWithRes(ViewTypeWithoutRes):
    up = None
    down = None
    train = None


class ViewWithtRes(ViewTypeWithRes, DB.DECLARATIVE_BASE):
    __table__ = Table("VJoinedVRes", DB.DECLARATIVE_BASE.metadata,
                        Column("id", Integer, primary_key=True),
                        autoload=True, autoload_with=DB.ENGINE,
                    )

    @staticmethod
    def get_test_candles() -> List[ViewTypeWithRes]:
        DB = DB.get_globals()
        test_candles = DB.SESSION.query(ViewWithtRes).filter(ViewWithtRes.train == False).order_by(asc(ViewWithtRes.open_time)).all()
        return test_candles

    @classmethod
    def get_test_candles_for_symbols(cls, symbols) -> List[ViewTypeWithRes]:
        train_expression = getattr(cls, "train") == False

        return DB.SESSION.query(ViewWithtRes).filter(and_(train_expression, ViewWithtRes.symbol.in_(symbols))).order_by(
            asc(ViewWithtRes.open_time)).all()

    @staticmethod
    def get_train_candles_for_symbol(symbol) -> List[ViewTypeWithRes]:
        DB = DB.get_globals()
        train_candles = DB.SESSION.query(ViewWithtRes).filter(
            and_(ViewWithtRes.symbol == symbol, ViewWithtRes.train == True)).order_by(
            asc(ViewWithtRes.open_time)).all()
        return train_candles

    @classmethod
    def get_train_candles(cls, symbols: List[str]):
        train_expression = getattr(cls, "train") == True
        return DB.SESSION.query(ViewWithtRes).filter(and_(train_expression, ViewWithtRes.symbol.in_(symbols))).order_by(
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
