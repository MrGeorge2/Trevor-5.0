from ..globals.config import Config
from ..data_analysis.models.views import ViewWithtRes
import tensorflow as tf


class Samples(ViewWithtRes):
    def __init__(self):
        self.cfg = Config()
        self.TIMESTEPS = self.cfg.TIMESTEPS


    @staticmethod
    def create_samples(*args):
        db = DB.get_globals()
        for symbol in random.samples(Config.SYMBOLS_TO_SCRAPE, self.RANDOM_SYMBOLS_FOR_SAMPLE):
            print(f"Creating samples from symbol={symbol}")

            
            candles: List[CandleApi] = db.SESSION.query(CandleApi).filter(CandleApi.symbol == symbol)
            """
            for i, candle in enumerate(candles):
                open_price = candle.open_price
                close_price = candle.close_price

                if Config.CHECK_ROW_IN_DB:

                    if not db.SESSION.query(db.SESSION.query(Results).filter(
            """
            print("hovno")