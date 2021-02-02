from decimal import Decimal
from typing import List
from datetime import datetime, timedelta
from .order import StopLossOrder, TakeProfitOrder, InitOrder,  Long, Short, Order, FullOrderBase
from ..globals.config import Config
from ..data_analysis.models.candle_api import CandleApi
import logging


class OrderManager:
    def __init__(self, symbol: str):
        self.symbol: str = symbol

        self.profitable_trades: int = 0
        self.not_profitable_trades: int = 0
        self.closed_orders: int = 0

        self.total_profit: Decimal = Decimal(0)
        self.opened_orders: List[FullOrderBase] = []

    def open_long(self, price: Decimal, take_profit: Decimal, stop_loss: Decimal):
        logging.info(f"Opening long init_price={round(price, 4)} take_profit={round(take_profit, 4)} stop_loss={round(stop_loss, 4)}")
        open_order = InitOrder(price=price, symbol=self.symbol)
        sl_order = StopLossOrder(price=stop_loss, symbol=self.symbol)
        tp_order = TakeProfitOrder(price=take_profit, symbol=self.symbol)

        long = Long(open_order, sl_order, tp_order)
        long.init_order.open()

        self.opened_orders.append(long)

    def open_short(self, price: Decimal, take_profit: Decimal, stop_loss: Decimal):
        logging.info(f"Opening short init_price={round(price, 4)} take_profit={round(take_profit, 4)} stop_loss={round(stop_loss, 4)}")
        open_order = InitOrder(price=price, symbol=self.symbol)
        sl_order = StopLossOrder(price=stop_loss, symbol=self.symbol)
        tp_order = TakeProfitOrder(price=take_profit, symbol=self.symbol)

        short = Short(open_order, sl_order, tp_order)
        short.init_order.open()

        self.opened_orders.append(short)

    def close_all_opened(self):
        pass

    def is_order_already_opened(self,  last_candle: CandleApi, prediction):
        better_opened = 0
        for order in self.opened_orders:
            if isinstance(order, Long) and prediction == 1:
                if order.init_order.price <= last_candle.close_price:
                    better_opened += 1

            elif isinstance(order, Short) and prediction == 0:
                if order.init_order.price >= last_candle.close_price:
                    better_opened += 1

        return better_opened > 0

    def check_opened_orders(self, last_candle: CandleApi):
        for order in self.opened_orders:
            if (datetime.now() - order.init_order.open_time) >= timedelta(minutes=Config.CANDLE_MINUTES_INTERVAL):
                order.close()
                if isinstance(order, Long):
                    profit = ((last_candle.close_price - order.init_order.price) / order.init_order.price) * 100
                    if profit > 0:
                        self.profitable_trades += 1

                    logging.info(f"Closing Long TIMEOUT\t profit={profit}")
                    self.total_profit += profit

                if isinstance(order, Short):
                    profit = (-1 * (last_candle.close_price - order.init_order.price) / order.init_order.price) * 100
                    if profit > 0:
                        self.profitable_trades += 1

                    logging.info(f"Closing SHORT TIMEOUT\t profit={profit}")
                    self.total_profit += profit

                self.closed_orders += 1
                self.opened_orders.pop((self.opened_orders.index(order)))

            else:
                if isinstance(order, Long):
                    if last_candle.high_price >= order.take_profit.price:
                        order.close()
                        self.total_profit += ((order.take_profit.price - order.init_order.price) / order.init_order.price) * 100    # v procentech

                        self.closed_orders += 1
                        self.opened_orders.pop((self.opened_orders.index(order)))
                        self.profitable_trades += 1
                        logging.info(f"Closing Long TP\tlast_candle.high_price={round(last_candle.high_price, 4)}\torder.take_profit={round(order.take_profit.price, 4)}")

                    elif last_candle.low_price <= order.stop_loss.price:
                        order.close()
                        self.total_profit -= ((order.init_order.price - order.stop_loss.price) / order.init_order.price) * 100    # v procentech

                        self.closed_orders += 1
                        self.opened_orders.pop((self.opened_orders.index(order)))
                        self.not_profitable_trades += 1
                        logging.info(f"Closing Long SL\tlast_candle.low_price={round(last_candle.low_price, 4)}\torder.stop_loss={round(order.stop_loss.price, 4)}")

                if isinstance(order, Short):
                    if last_candle.low_price <= order.take_profit.price:
                        order.close()
                        self.total_profit += ((order.init_order.price - order.take_profit.price) / order.init_order.price) * 100  # v procentech

                        self.closed_orders += 1
                        self.opened_orders.pop((self.opened_orders.index(order)))
                        self.profitable_trades += 1
                        logging.info(f"Closing SHORT TP\tlast_candle.low_price={round(last_candle.low_price,4)}\torder.take_profit={round(order.take_profit.price, 4)}")

                    elif last_candle.high_price >= order.stop_loss.price:
                        order.close()
                        self.total_profit -= ((order.stop_loss.price - order.init_order.price) / order.init_order.price) * 100  # v procentech

                        self.closed_orders += 1
                        self.opened_orders.pop((self.opened_orders.index(order)))
                        self.not_profitable_trades += 1
                        logging.info(f"Closing SHORT SL\tlast_candle.low_price={round(last_candle.high_price, 4)}\torder.stop_loss={round(order.stop_loss.price, 4)}")

