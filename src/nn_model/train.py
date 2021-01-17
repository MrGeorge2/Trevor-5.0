from ..globals.config import Config
from .modelnn import ModelNN
from ..samples.samples import Samples
from ..data_analysis.models.views import ViewWithtRes
from ..data_analysis.models.train_log import TrainLog
from ..utils.tread import ReturningThread


class TrainNN:
    @classmethod
    def train(cls):
        model = ModelNN()
        model.load()
        print("Creating test dataset for BTCUSDT")
        btc_usdt_test_samples = ViewWithtRes.get_test_candles_for_symbols(['BTCUSDT'])
        btc_usdt_test_samples = Samples.create_samples(btc_usdt_test_samples)
        model.set_test_samples(btc_usdt_test_samples)
        print("Test dataset created")

        first = True
        for i in range(Config.ITERATIONS_CANLED_GROUP):
            for symbol_index, symbols in enumerate(Config.SYMBOL_GROUPS_1H):
                # Load samples before training only first time
                if first:
                    sample_thread = ReturningThread(target=Samples.create_samples_for_symbols, args=(Config.SYMBOL_GROUPS_1H[0], ))
                    sample_thread.start()
                    first = False

                model.set_train_samples(sample_thread.join())
                next_symbols = Config.SYMBOL_GROUPS_1H[symbol_index + 1] if symbol_index + 1 < len(
                    Config.SYMBOL_GROUPS_1H) else Config.SYMBOL_GROUPS_1H[0]
                sample_thread = ReturningThread(target=Samples.create_samples_for_symbols, args=(next_symbols,))
                sample_thread.start()
                model.train()

            TrainNN.eval(model)
            model.show_real_output()
            model.set_test_samples(btc_usdt_test_samples)

    @classmethod
    def train_on_few_samples(cls):
        model = ModelNN()
        model.load()
        print("Creating test dataset for BTCUSDT")
        btc_usdt_test_samples = ViewWithtRes.get_test_candles_for_symbols(['BTCUSDT'])
        btc_usdt_test_samples = Samples.create_samples(btc_usdt_test_samples)
        model.set_test_samples(btc_usdt_test_samples)
        print("Test dataset created")

        first = True
        for i in range(Config.ITERATIONS_CANLED_GROUP):
            for symbols in Config.SYMBOL_GROUPS_1H[0]:
                # Load samples before training only first time
                if first:
                    sample_thread = ReturningThread(target=Samples.create_samples_for_symbols, args=(Config.SYMBOL_GROUPS_1H[0], ))
                    sample_thread.start()
                    first = False
                model.set_train_samples(sample_thread.join())
                
                model.x_train = model.x_train[:Config.NUMBER_OF_SAMPLES_FOR_NN_TEST, :, :]
                model.y_train = model.y_train[:Config.NUMBER_OF_SAMPLES_FOR_NN_TEST, :]
                for i in range(10000):
                    model.train()

            TrainNN.eval(model)
            model.show_real_output()
            model.set_test_samples(btc_usdt_test_samples)


    @staticmethod
    def eval(model):
        print("Evaluate")
        for symbols in Config.SYMBOL_GROUPS_1H:
            test_candles = ViewWithtRes.get_test_candles_for_symbols(symbols)
            test_samples = Samples.create_samples(test_candles)

            model.set_test_samples(test_samples)
            model.eval(' '.join(symbols), "")
        print("Evaluate done")

