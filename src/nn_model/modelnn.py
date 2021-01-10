from ..globals.config import Config
import os
from sqlalchemy import asc, and_
import numpy as np
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from ..samples.samples import Samples
from ..data_analysis.models.views import ViewWithtRes
from ..utils.tread import ReturningThread


class ModelNN:
    def __init__(self):   # TODO: oddelat None - je to tam kvuli testu
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []

        self.model = self.model_load()
        # self.print_unique()

    def set_train_samples(self, train_samples):
        self.x_train = train_samples[0]
        self.y_train = train_samples[1]

    def set_test_samples(self, test_samples):
        self.x_test = test_samples[0]
        self.y_test = test_samples[1]

    def print_unique(self):
        unique, counts = np.unique(self.y_train, return_counts=True)
        print(f"Četnosti kategorií v tréninkovém datasetu: {dict(zip(unique, counts))}")

    def model_load(self):
        if os.path.isfile(Config.PATH_MODEL):
            model = load_model(Config.PATH_MODEL)
            print("Model loaded.")
            return model
        else:
            self.create_model()
            self.model = self.model_load()

    def model_save(self):
        self.model.save(Config.PATH_MODEL)
        print("Model saved.")

    def create_model(self):
        self.model = Sequential()
        self.model.add(LSTM(units=128, return_sequences=True, input_shape=(Config.TIMESTEPS, Config.FINAL_SAMPLE_COLUMNS)))
        self.model.add(Dropout(0.1))
        self.model.add(LSTM(units=64, return_sequences=True))
        self.model.add(Dropout(0.1))
        self.model.add(LSTM(units=64, return_sequences=True))
        self.model.add(Dropout(0.1))
        self.model.add(LSTM(units=64, return_sequences=False))
        self.model.add(Dropout(0.1))

        self.model.add(Dense(units=64, activation="relu"))
        self.model.add(Dropout(0.1))
        self.model.add(Dense(units=32, activation="relu"))
        self.model.add(Dropout(0.1))
        self.model.add(Dense(units=16, activation="relu"))
        self.model.add(Dropout(0.1))
        self.model.add(Dense(units=8, activation="relu"))
        self.model.add(Dropout(0.1))

        self.model.add(Dense(units=2, activation='softmax'))
        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=["accuracy"])
        print("Model created.")
        self.model_save()

    def train_model(self):
        self.model.fit(self.x_train, self.y_train, epochs=Config.EPOCHS, batch_size=10, validation_data=(self.x_test, self.y_test))
        self.model_save()


class TrainNN:
    @classmethod
    def train_async(cls):
        print("Creating test samples")
        test_candles = ViewWithtRes.get_test_candles()
        test_samples = Samples.create_samples(test_candles)
        print("Test samples created")

        model = ModelNN()
        model.model_load()
        model.set_test_samples(test_samples)

        first = True
        for i in range(Config.ITERATIONS_CANLED_GROUP):
            for symbol_index, symbols in enumerate(Config.SYMBOL_GROUPS):
                # Nacteni symbolu pred treninkem pouze poprve
                if first:
                    sample_thread = ReturningThread(target=cls.get_training_samples, args=(Config.SYMBOL_GROUPS[0], ))
                    sample_thread.start()
                    first = False

                # train_candles = ViewWithtRes.get_train_candles(symbols)
                # train_samples = Samples.create_samples(train_candles)

                model.set_train_samples(sample_thread.join())
                next_symbols = Config.SYMBOL_GROUPS[symbol_index] if symbol_index + 1 <= len(Config.SYMBOL_GROUPS) else Config.SYMBOL_GROUPS[0]
                sample_thread = ReturningThread(target=cls.get_training_samples, args=(next_symbols,))
                sample_thread.start()
                model.train_model()

    @classmethod
    def train(cls):
        cls.train_async()

    @staticmethod
    def get_training_samples(symbols):
        print(f"Creating samples for symbol group {symbols}")
        train_candles = ViewWithtRes.get_train_candles(symbols)
        train_samples = Samples.create_samples(train_candles)
        print(f"Created samples for symbol group")
        return train_samples