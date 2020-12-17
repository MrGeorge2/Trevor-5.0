from sqlalchemy import Column, String, DateTime, DECIMAL, Integer
from .object_base import ObjectBase


class CandleApi(ObjectBase):
    __tablename__ = "TCandleApi"
    open_time = Column(Integer)
    open_price = Column(DECIMAL)
    high_price = Column(DECIMAL)
    low_price = Column(DECIMAL)
    close_price = Column(DECIMAL)
    volume = Column(DECIMAL)
    close_time = Column(Integer)
    quote_asset_volume = Column(DECIMAL)
    number_of_trades = Column(DECIMAL)
    taker_buy_base_asset_volume = Column(DECIMAL)
    taker_buy_quote_asset_volume = Column(DECIMAL)