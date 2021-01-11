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
            TrainNN.eval()

    @staticmethod
    def eval():
        model = ModelNN()
        model.load()

        print("Evaluate")
        for symbols in Config.SYMBOL_GROUPS_1H:
            test_candles = ViewWithtRes.get_test_candles_for_symbols(symbols)
            test_samples = Samples.create_samples(test_candles)

            model.set_test_samples(test_samples)
            model.eval(' '.join(symbols), "")
        print("Evaluate done")
