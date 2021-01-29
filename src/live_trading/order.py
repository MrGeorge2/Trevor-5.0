from datetime import datetime


class Order:
    CLOSED = False
    SYMBOL = None

    OPEN_TIME = None
    CLOSE_TIME = None
    OPEN_PRICE: float = 0
    CLOSE_PRICE: float = 0

    def __init__(self, open_price, symbol):
        self.OPEN_PRICE = open_price
        self.SYMBOL = symbol
        self.OPEN_TIME = datetime.now()

    def close(self, close_price):
        self.CLOSE_PRICE = close_price
        self.CLOSE_TIME = datetime.now()
        self.CLOSED = True

    def is_closed(self) -> bool:
        return True if self.CLOSED else False

    def get_profit(self) -> float:
        return self.CLOSE_PRICE - self.OPEN_PRICE


    #TODO: ziskat svicky z api
    #TODO: preprocessing
    #TODO: narvat to do nn
    #TODO: metody pro orders
    #TODO: sledovani zisku