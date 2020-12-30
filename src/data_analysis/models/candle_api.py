from ...globals.db import DB
from sqlalchemy import Column,  DECIMAL, Integer, DATETIME, String


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
