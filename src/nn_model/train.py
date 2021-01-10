from ..globals.config import Config
from .modelnn import ModelNN
from ..samples.samples import Samples
from ..data_analysis.models.views import ViewWithtRes
from ..utils.tread import ReturningThread


class TrainNN:
    @classmethod
    def train(cls):
        print("Creating test samples")
        test_candles = ViewWithtRes.get_test_candles()
        test_samples = Samples.create_samples(test_candles)
        print("Test samples created")

        model = ModelNN()
        model.load()
        model.set_test_samples(test_samples)

        first = True
        for i in range(Config.ITERATIONS_CANLED_GROUP):
            for symbol_index, symbols in enumerate(Config.SYMBOL_GROUPS):
                # Load samples before training only first time
                if first:
                    sample_thread = ReturningThread(target=Samples.create_samples_for_symbols, args=(Config.SYMBOL_GROUPS[0], ))
                    sample_thread.start()
                    first = False

                model.set_train_samples(sample_thread.join())
                next_symbols = Config.SYMBOL_GROUPS[symbol_index] if symbol_index + 1 <= len(Config.SYMBOL_GROUPS) else Config.SYMBOL_GROUPS[0]
                sample_thread = ReturningThread(target=Samples.create_samples_for_symbols, args=(next_symbols,))
                sample_thread.start()
                model.train()
