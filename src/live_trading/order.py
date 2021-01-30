from datetime import datetime
from ..globals.config import Config
from binance.enums import ORDER_TYPE_MARKET
from typing import Optional
from decimal import Decimal


class Order:

    def __init__(self, open_price: Decimal, symbol: str, order_type: str):
        self.open_price: Decimal = open_price
        self.symbol: str = symbol
        self.open_time: datetime = datetime.now()
        self.order_type: str = order_type
        self._order_id: Optional[str] = None

        self.closed: Optional[bool] = False
        self.close_price: Optional[Decimal] = None
        self.close_time: Optional[datetime] = None

    def set_order_id(self, order_id):
        self._order_id = order_id

    def open(self):
        pass

    def close(self, close_price):
        self.close_price = close_price
        self.close_time = datetime.now()
        self.closed = True

    @property
    def is_filled(self) -> bool:
        return True

    @property
    def is_closed(self) -> bool:
        return self.closed

    def get_profit(self) -> float:
        if self.is_closed:
            return (Decimal(self.close_price - self.open_price) / self.open_price) * 100
        else:
            Decimal(0)


class InitOrder(Order):
    pass


class StopLossOrder(Order):
    pass


class TakeProfitOrder(Order):
    pass


class Long:
    def __init__(self, init_order: InitOrder, stop_loss: StopLossOrder, take_profit: TakeProfitOrder):
        self.init_order = init_order
        self.stop_loss = stop_loss
        self.take_profit = take_profit


class Short:
    def __init__(self, init_order: InitOrder, stop_loss: StopLossOrder, take_profit: TakeProfitOrder):
        self.init_order = init_order
        self.stop_loss = stop_loss
        self.take_profit = take_profit

#TODO: ziskat svicky z api
    #TODO: preprocessing
    #TODO: narvat to do nn
    #TODO: metody pro orders
    #TODO: sledovani zisku