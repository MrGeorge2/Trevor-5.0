from decimal import Decimal
from typing import Sequence
from .order import StopLossOrder, TakeProfitOrder, InitOrder,  Long, Short, Order


class OrderManager:
    def __init__(self):
        self.total_profit = 0
        self.opened_orders: Sequence[Order] = []
        self.closed_orders: Sequence[Order] = []

    def open_long(self, open_price: Decimal, take_profit: Decimal, stop_loss: Decimal):
        """
        open_order = InitOrder()
        sl_order = StopLossOrder()
        tp_order = TakeProfitOrder()

        long = Long(open_order, sl_order, tp_order)
        long.init_order.open()
        """
        pass

    def open_short(self, open_price: Decimal, take_profit: Decimal, stop_loss: Decimal):
        """
        open_order = InitOrder()
        sl_order = StopLossOrder()
        tp_order = TakeProfitOrder()

        short = Short(open_order, sl_order, tp_order)
        short.init_order.open()
        """
        pass

    def close_all_opened(self):
        pass

    def check_opened_orders(self):
        pass
