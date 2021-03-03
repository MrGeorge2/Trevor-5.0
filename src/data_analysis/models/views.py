from ...globals.db import DB
from ...globals.config import Config
from sqlalchemy import Table, Column, Integer, asc, and_, or_
from typing import List
import numpy as np


class ViewTypeWithoutRes:
    id = None
    symbol = None
    open_time = None
    open_price = None
    high_price = None
    low_price = None
    close_price = None
    volume = None

class ViewTypeWithRes(ViewTypeWithoutRes):
    up = None
    down = None
    train = None

    def get_features(self):
        attribs_to_return = [
            # ViewTypeWithRes.normalize_time(self.open_time),
            self.open_price,
            self.high_price,
            self.low_price,
            self.close_price,
            self.volume,
        ]

        return np.asarray([attribs_to_return], dtype=np.float32)

    def get_results(self):
        attribs_to_return = [
            self.up,
            self.down
        ]

        return np.asarray(attribs_to_return, dtype=np.float32)

    def get_as_dict(self):
        return {
            'open_price': float(self.open_price),
            'high_price': float(self.high_price),
            'low_price': float(self.low_price),
            'close_price': float(self.close_price),
            'volume': float(self.volume),
            "target": np.float64(self.up),
        }

    @staticmethod
    def normalize_time(dt):
        """
        0-24 hod do rozsahu 0-1
        """
        normalized_time = float(dt.hour*3600+dt.minute*60+dt.second)/86400
        return normalized_time


db = DB.get_globals()


class ViewWithtRes(ViewTypeWithRes, db.DECLARATIVE_BASE):
    __table__ = Table("VJoinedVRes", db.DECLARATIVE_BASE.metadata,
                        Column("id", Integer, primary_key=True),
                        autoload=True, autoload_with=db.ENGINE,
                    )

    @staticmethod
    def get_test_candles() -> List[ViewTypeWithRes]:
        dbb = DB.get_globals()
        test_candles = dbb.SESSION.query(ViewWithtRes).filter(ViewWithtRes.train == False).order_by(asc(ViewWithtRes.open_time)).all()
        return test_candles

    @classmethod
    def get_test_candles_for_symbols(cls, symbols) -> List[ViewTypeWithRes]:
        train_expression = getattr(cls, "train") == False
        dbb = DB.get_globals()
        return dbb.SESSION.query(ViewWithtRes).filter(
            and_(train_expression, ViewWithtRes.symbol.in_(symbols))).order_by(asc(ViewWithtRes.open_time)).all()

    @staticmethod
    def get_train_candles_for_symbol(symbol) -> List[ViewTypeWithRes]:
        dbb = DB.get_globals()
        train_candles = dbb.SESSION.query(ViewWithtRes).filter(
            and_(ViewWithtRes.symbol == symbol, ViewWithtRes.train == True)).order_by(
            asc(ViewWithtRes.open_time)).all()
        return train_candles

    @classmethod
    def get_train_candles(cls, symbols: List[str]):
        dbb = DB.get_globals()
        train_expression = getattr(cls, "train") == True
        return dbb.SESSION.query(ViewWithtRes).filter(
            and_(train_expression, ViewWithtRes.symbol.in_(symbols))).order_by(asc(ViewWithtRes.open_time)).all()

    def __repr__(self):
        return f"symbol={self.symbol} open_time={self.open_time} up={self.up} down={self.down}"


"""
Priklad pouziti.. dulezite je pridat typ List[ViewTypeWithRes] potom to bude radit typy
def test(*args):
    res: List[ViewTypeWithRes] = DB.SESSION.query(ViewWithtRes)
    for r in res:
        print(r.symbol)
"""
