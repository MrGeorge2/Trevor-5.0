from ...globals.db import DB
from .candle_api import CandleApi
from ...globals.config import Config
from sqlalchemy import Column, Boolean, DATETIME, Integer, String, ForeignKey, and_
from typing import List
from random import sample


class Results(DB.DECLARATIVE_BASE):
    __tablename__ = "TResults"
    id = Column(Integer, primary_key=True)
    up = Column(Boolean)
    down = Column(Boolean)
    open_time = Column(DATETIME, ForeignKey(CandleApi.open_time))
    symbol = Column(String, ForeignKey(CandleApi.symbol))
    train = Column(Boolean)

    def __repr__(self):
        return f"up={self.up} down={self.down} open_time={self.open_time} symbol={self.symbol}"

    @staticmethod
    def count_results(*args):
        db = DB.get_globals()
        for symbol in Config.SYMBOLS_TO_SCRAPE:
            print(f"Counting results for symbol={symbol}")
            candles: List[CandleApi] = db.SESSION.query(CandleApi).filter(CandleApi.symbol == symbol)

            for i, candle in enumerate(candles):
                open_price = candle.open_price
                close_price = candle.close_price

                if Config.CHECK_ROW_IN_DB:

                    if not db.SESSION.query(db.SESSION.query(Results).filter(
                            and_(Results.symbol == candle.symbol,
                                 Results.open_time == candle.open_time)).exists()).scalar():

                        if open_price > close_price:
                            res = Results(up=False, down=True, open_time=candle.open_time, symbol=candle.symbol)

                        elif open_price < close_price:
                            res = Results(up=True, down=False, open_time=candle.open_time, symbol=candle.symbol)
                        else:
                            res = Results(up=False, down=False, open_time=candle.open_time, symbol=candle.symbol)
                        db.SESSION.add(res)
                else:
                    if open_price > close_price:
                        res = Results(up=False, down=True, open_time=candle.open_time, symbol=candle.symbol)

                    elif open_price < close_price:
                        res = Results(up=True, down=False, open_time=candle.open_time, symbol=candle.symbol)
                    else:
                        res = Results(up=False, down=False, open_time=candle.open_time, symbol=candle.symbol)
                    db.SESSION.add(res)

            print("Done")
            db.SESSION.commit()

    @staticmethod
    def divide_train_test(*args):
        db = DB.get_globals()
        for symbol in Config.SYMBOLS_TO_SCRAPE:
            results: List[Results] = db.SESSION.query(Results).filter(Results.symbol == symbol).all()
            print(f"Dividing train test for {symbol}")

            train_samples = sample(results, int(len(results) * 0.8))
            test_samples = [candle for candle in results if candle not in train_samples]

            for candle in train_samples:
                setattr(candle, "train", True)

            for candle in test_samples:
                setattr(candle, "train", False)
        DB.SESSION.commit()
        print("Done")
