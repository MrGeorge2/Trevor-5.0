from ..globals.config import Config
from ..data_analysis.models.views import ViewWithtRes, ViewTypeWithRes
from typing import List
from numpy import mean, median, argmax, reshape
from ..nn_model.modelnn import ModelNN
from ..samples.samples import Samples


class BackTest:
    MAX_DROP = 0
    MAX_RAISE = 0

    def __init__(self, test_data: List[ViewTypeWithRes]):
        self.test_data = test_data

    def analyze_avg_percent_changes_sl_tp(self):
        max_drops = []
        max_raises = []

        for i in range(len(self.test_data)):
            if i + Config.NUMBER_FUTURE_CANDLE_PREDICT >= len(self.test_data):
                break

            act_drop = 0
            act_raise = 0

            act_candle = self.test_data[i]
            for iter_candle in self.test_data[i + 1: i + Config.NUMBER_FUTURE_CANDLE_PREDICT]:
                temp_drop = ((iter_candle.low_price - act_candle.open_price) * 100) / act_candle.open_price
                temp_raise = ((iter_candle.close_price - act_candle.open_price) * 100) / act_candle.open_price

                if temp_drop < act_drop:
                    act_drop = temp_drop

                if temp_raise > act_raise:
                    act_raise = temp_raise

            max_drops.append(act_drop)
            max_raises.append(act_raise)

        avg_drop = mean(max_drops)
        median_drop = median(max_drops)

        avg_raise = mean(max_raises)
        median_raise = median(max_raises)

        print(f"avg_drop={avg_drop} median_drop={median_drop} avg_raise={avg_raise} median_raise={median_raise}")
        return avg_drop, median_drop, avg_raise, median_raise

    def full_back_test(self):
        final_percentage = 0
        day_counter = 0
        trade_counter = 0
        model = ModelNN()
        model.load()
        test_samples = Samples.create_samples(self.test_data, False)[0]

        for i in range(Config.TIMESTEPS, len(self.test_data)):
            if i + Config.NUMBER_FUTURE_CANDLE_PREDICT >= len(self.test_data):
                break

            sequence_to_predict = reshape(test_samples[Config.TIMESTEPS - i], (1, Config.TIMESTEPS, Config.FINAL_SAMPLE_COLUMNS))
            sequence_backtest = self.test_data[i: ]

            prediction = model.model.predict(sequence_to_predict)
            predicted = argmax(prediction)
            certainty = max(prediction[0])

            trade_closed = False
            for j, iter_candle in enumerate(sequence_backtest):
                if j + 1 >= len(sequence_backtest):
                    break
                next_candle = sequence_backtest[j + 1]

                temp_drop = ((iter_candle.low_price - next_candle.open_price) * 100) / iter_candle.open_price
                temp_raise = ((iter_candle.close_price - next_candle.open_price) * 100) / iter_candle.open_price

                # UP
                if predicted == 1:
                    # SL CHECK
                    if temp_drop <= self.MAX_DROP:
                        final_percentage += self.MAX_DROP
                        trade_closed = True
                        break

                    # TP CHECK
                    elif temp_raise >= self.MAX_RAISE:
                        final_percentage += self.MAX_RAISE
                        trade_closed = True
                        break

                # DOWN
                else:
                    # SL CHECK
                    if temp_raise >= self.MAX_RAISE:
                        final_percentage -= self.MAX_RAISE
                        trade_closed = True
                        break

                    # TP CHECK
                    elif temp_drop <= self.MAX_DROP:
                        final_percentage -= self.MAX_DROP
                        trade_closed = True
                        break

            if not trade_closed:
                open_candle = sequence_backtest[0]
                close_candle = sequence_backtest[-1]

                percentage_gain = (close_candle.close_price - open_candle.open_price) * 100 / open_candle.open_price
                final_percentage += percentage_gain

            trade_counter += 1
            day_counter += 1
            print(f"certainty={certainty} temp_percentage={final_percentage} trade_counter={trade_counter} days={day_counter / 1440}")

        print(f"final_percentage={final_percentage} trade_counter={trade_counter} days={day_counter / 1440}")
        return final_percentage


def count_average_movements():
    test_candles = ViewWithtRes.get_test_candles()
    bccktest = BackTest(test_candles)
    return bccktest.analyze_avg_percent_changes_sl_tp()


def backtest():
    avg_drop, median_drop, avg_raise, median_raise = count_average_movements()
    test_candles = ViewWithtRes.get_test_candles()

    bcktest = BackTest(test_candles)
    bcktest.MAX_DROP = avg_raise
    bcktest.MAX_RAISE = avg_raise

    bcktest.full_back_test()
