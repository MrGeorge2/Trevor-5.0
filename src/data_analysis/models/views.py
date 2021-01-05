from ...globals.db import DB
from sqlalchemy import Table, Column, Integer, String, DATETIME, DECIMAL, Boolean
from typing import List
import random


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
    sma21 = None
    sma200 = None
    ema21 = None
    ema200 = None


class ViewWithoutRes(ViewTypeWithoutRes, db.DECLARATIVE_BASE):
    __table__ = Table("VJoined", db.DECLARATIVE_BASE.metadata,
                      Column("id", Integer, primary_key=True),
                             autoload=True, autoload_with=db.ENGINE
                    )


class ViewTypeWithRes(ViewTypeWithoutRes):
    up = None
    down = None
    train = None


class ViewWithtRes(ViewTypeWithRes, DB.DECLARATIVE_BASE):
    __table__ = Table("VJoinedVRes", DB.DECLARATIVE_BASE.metadata,
                        Column("id", Integer, primary_key=True),
                        autoload=True, autoload_with=db.ENGINE,
                    )

    def __repr__(self):
        return f"symbol={self.symbol} open_time={self.open_time} up={self.up} down={self.down}"


"""
Priklad pouziti.. dulezite je pridat typ List[ViewTypeWithRes] potom to bude radit typy
def test(*args):
    res: List[ViewTypeWithRes] = db.SESSION.query(ViewWithtRes)
    for r in res:
        print(r.symbol)
"""
