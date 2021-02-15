from ...globals.db import DB
from .candle_api import CandleApi
from ...globals.config import Config
from sqlalchemy import Column, Boolean, DATETIME, Integer, String, ForeignKey, DECIMAL, and_, between, asc
from typing import List
from decimal import Decimal
from ...utils.day_counter import DayCounter
from dateparser.date import DateDataParser


class Results(DB.DECLARATIVE_BASE):
    __tablename__ = "TResults"
    id = Column(Integer, primary_key=True)
    up = Column(DECIMAL)
    down = Column(DECIMAL)
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
            candles: List[CandleApi] = db.SESSION.query(CandleApi).filter(and_(CandleApi.symbol == symbol)).order_by(asc(CandleApi.open_time)).all()

            for i, candle in enumerate(candles):
                if i + Config.NUMBER_FUTURE_CANDLE_PREDICT < len(candles):
                    next_candles = candles[i: i + Config.NUMBER_FUTURE_CANDLE_PREDICT]
                else:
                    break

                # if Config.CHECK_ROW_IN_DB:

                    # if not db.SESSION.query(db.SESSION.query(Results).filter(
                     #       and_(Results.symbol == candle.symbol,
                     #            Results.open_time == candle.open_time)).exists()).scalar():

                up = Decimal(round((max([candle.high_price for candle in next_candles]) - candle.close_price) / candle.close_price * 100), 3)
                down = Decimal(round((candle.close_price - min([candle.low_price for candle in next_candles])) / candle.close_price * 100), 3)

                res = Results(up=up, down=down, open_time=candle.open_time, symbol=candle.symbol)
                db.SESSION.add(res)

            print("Done")
            db.SESSION.commit()

    @staticmethod
    def divide_train_test(*args):
        db = DB.get_globals()
        for symbol in Config.SYMBOLS_TO_SCRAPE:
                results: List[Results] = db.SESSION.query(Results).filter(and_(Results.symbol == symbol)).all()
                print(f"Dividing train test for {symbol}")

                test_samples = results[int(len(results) * 0.85): ]
                # train_samples = sample(results, int(len(results) * 0.85))
                train_samples = [candle for candle in results if candle not in test_samples]

                for candle in train_samples:
                    setattr(candle, "train", True)

                for candle in test_samples:
                    setattr(candle, "train", False)
        DB.SESSION.commit()
        print("Done")

    @staticmethod
    def reverse_train_data(*args):
        db = DB.get_globals()
        for symbol in Config.SYMBOLS_TO_SCRAPE:
            print(f"Reversing train-test for symbol {symbol}")
            results: List[Results] = db.SESSION.query(Results).filter(Results.symbol == symbol).all()
            for candle in results:
                setattr(candle, "train", not candle.train)
            db.SESSION.commit()



