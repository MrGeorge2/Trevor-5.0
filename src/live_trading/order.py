from datetime import datetime
from ..globals.config import Config
from binance.enums import ORDER_TYPE_MARKET
from typing import Optional
from decimal import Decimal


class OrderInterface:
    # ORDER_TYPE: str = ORDER_TYPE_MARKET.maketrans()  # TODO: nejak vymyslet, jak to ma byt pro futures market

    def set_order_id(self):
        pass

    def open(self):
        pass

    def close(self):
        pass

    @property
    def is_opened(self) -> bool:
        return False

    @property
    def is_filled(self) -> bool:
        return False

    @property
    def is_closed(self) -> bool:
        return False


class Order(OrderInterface):
    def __init__(self, price: Decimal, symbol: str):
        self.price: Decimal = price
        self.symbol: str = symbol
        self.open_time: datetime = datetime.now()

        self._order_id: Optional[str] = None

        self.filled: Optional[bool] = False
        self.closed: Optional[bool] = False
        self.close_time: Optional[datetime] = None

    def set_order_id(self, order_id):
        self._order_id = order_id

    def open(self):
        pass

    def close(self):
        if self.is_opened:
            self.close_time = datetime.now()
            self.closed = True

    @property
    def is_filled(self) -> bool:
        return self.filled

    @property
    def is_closed(self) -> bool:
        return self.closed


class InitOrder(Order):
    pass


class StopLossOrder(Order):
    pass


class TakeProfitOrder(Order):
    pass


class FullOrderBase(OrderInterface):
    def __init__(self, init_order: InitOrder, stop_loss: StopLossOrder, take_profit: TakeProfitOrder):
        self.init_order = init_order
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    def get_profit(self) -> float:
        if self.stop_loss.is_filled:
            return Decimal(self.stop_loss.price - self.init_order.price) / self.init_order.price  # * 100
        elif self.take_profit.is_filled:
            return Decimal(self.stop_loss.price - self.init_order.price) / self.init_order.price  # * 100
        else:
            Decimal(0)

    def open(self):
        self.init_order.open()
        self.stop_loss.open()

    def close(self):
        self.init_order.close()
        self.take_profit.close()
        self.stop_loss.close()

    def open_stop_loss(self):
        self.take_profit.close()
        self.stop_loss.open()

    def open_take_profit(self):
        self.stop_loss.close()
        self.take_profit.open()


class Long(FullOrderBase):
    pass


class Short(FullOrderBase):
    pass
