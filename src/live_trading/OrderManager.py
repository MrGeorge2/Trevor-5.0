from decimal import Decimal
from typing import List
from datetime import datetime, timedelta
from .order import StopLossOrder, TakeProfitOrder, InitOrder,  Long, Short, Order, FullOrderBase
from ..globals.config import Config
from ..data_analysis.models.candle_api import CandleApi


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
        for order in self.opened_orders:
            order.close()

    def check_opened_orders(self, last_candle: CandleApi):
        for order in self.opened_orders:
            if (datetime.now() - order.init_order.open_time) >= timedelta(minutes=Config.CANDLE_MINUTES_INTERVAL):
                order.close()
                self.total_profit += (last_candle.close_price - order.init_order.price) / order.init_order.price

                self.closed_orders.append(order)
                self.opened_orders.pop((self.opened_orders.index(order)))

            else:
                if last_candle.high_price >= order.take_profit.price:
                    order.close()
                    self.total_profit += ((order.take_profit.price - order.init_order.price) / order.init_order.price) * 100    # v procentech

                    self.closed_orders.append(order)
                    self.opened_orders.pop((self.opened_orders.index(order)))

                if last_candle.low_price <= order.stop_loss.price:
                    order.close()
                    self.total_profit -= ((order.init_order.price - order.stop_loss.price) / order.init_order.price) * 100    # v procentech

                    self.closed_orders.append(order)
                    self.opened_orders.pop((self.opened_orders.index(order)))
