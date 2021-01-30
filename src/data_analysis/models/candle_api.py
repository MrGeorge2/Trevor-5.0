from ...globals.db import DB
from sqlalchemy import Column,  DECIMAL, Integer, DATETIME, String
import numpy as np


class CandleApi(DB.DECLARATIVE_BASE):
    __tablename__ = "TCandleApi"
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    open_time = Column(DATETIME)
    open_price = Column(DECIMAL)
    high_price = Column(DECIMAL)
    low_price = Column(DECIMAL)
    close_price = Column(DECIMAL)
    volume = Column(DECIMAL)
    close_time = Column(DATETIME)
    quote_asset_volume = Column(DECIMAL)
    number_of_trades = Column(DECIMAL)
    taker_buy_base_asset_volume = Column(DECIMAL)
    taker_buy_quote_asset_volume = Column(DECIMAL)

    def __repr__(self):
        return f"open_time={self.open_time} close_time={self.close_time} open={self.open_price} " \
               f"high={self.high_price} low={self.low_price} close={self.close_price}"

    def prices_as_dict(self):
        return {
            'open_time': self.open_time,
            'open_price': float(self.open_price),
            'high_price': float(self.high_price),
            'low_price': float(self.low_price),
            'close_price': float(self.close_price),
            'volume': float(self.volume),
        }

    def prices_as_dict_live(self):
        return {
            "open_price": np.float64(self.open_price),
            "high_price": np.float64(self.high_price),
            "low_price": np.float64(self.low_price),
            "close_price": np.float64(self.close_price),
            "volume": np.float64(self.volume),
            "target": 0,
        }