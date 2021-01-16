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
    sma21 = Column(DECIMAL)
    sma200 = Column(DECIMAL)
    ema21 = Column(DECIMAL)
    ema200 = Column(DECIMAL)
    open_time = Column(DATETIME, ForeignKey(CandleApi.open_time))
    symbol = Column(String, ForeignKey(CandleApi.symbol))

    def __repr__(self):
        return f"sma21={self.sma21} sma200={self.sma200} ema21={self.ema21} ema200={self.ema200} " \
               f"open_time={self.open_time} symbol={self.symbol}"

    @staticmethod
    def count_ema(candle_actual: CandleApi, sma: Decimal, n: int):
        k = Decimal(2 / (n + 1))
        return ((candle_actual.close_price - sma) * k) + sma

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