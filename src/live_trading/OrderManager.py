from decimal import Decimal
from typing import Sequence
from typing import List
from .order import StopLossOrder, TakeProfitOrder, InitOrder,  Long, Short, Order, FullOrderBase


class OrderManager:
    def __init__(self, symbol: str):
        self.symbol: str = symbol
        self.total_profit: Decimal = Decimal(0)
        self.opened_orders: List[FullOrderBase] = []
        self.closed_orders: List[FullOrderBase] = []

    def open_long(self, price: Decimal, take_profit: Decimal, stop_loss: Decimal):

        open_order = InitOrder(price=price, symbol=self.symbol)
        sl_order = StopLossOrder(price=stop_loss, symbol=self.symbol)
        tp_order = TakeProfitOrder(price=take_profit, symbol=self.symbol)

        long = Long(open_order, sl_order, tp_order)
        long.init_order.open()

        self.opened_orders.append(long)

    def open_short(self, price: Decimal, take_profit: Decimal, stop_loss: Decimal):

        open_order = InitOrder(price=price, symbol=self.symbol)
        sl_order = StopLossOrder(price=stop_loss, symbol=self.symbol)
        tp_order = TakeProfitOrder(price=take_profit, symbol=self.symbol)

        short = Short(open_order, sl_order, tp_order)
        short.init_order.open()

        self.opened_orders.append(short)

    def close_all_opened(self):
        pass

    def check_opened_orders(self):
        pass
