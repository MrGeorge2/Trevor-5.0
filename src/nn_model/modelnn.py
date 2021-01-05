from ..globals.config import Config
import os
from sqlalchemy import asc, and_
import numpy as np
from keras.models import load_model, Sequential
from keras.layers import Dense, LSTM, Dropout
from ..samples.samples import Samples
from ..data_analysis.models.views import ViewWithtRes
from ..globals.db import DB
import random


class ModelNN:
    def __init__(self, x_train=None, y_train=None, x_test=None, y_test=None):   # TODO: oddelat None - je to tam kvuli testu
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test

        self.model = self.model_load()
        # self.print_unique()

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


class TestNN:
    @staticmethod
    def test_model_load():
        db = DB.get_globals()
        for symbol in random.sample(Config.SYMBOLS_TO_SCRAPE, Config.RANDOM_SYMBOLS_FOR_SAMPLE):
            print(f"Creating samples from symbol={symbol}")

            test_candles = db.SESSION.query(ViewWithtRes).filter(
                and_(ViewWithtRes.symbol == symbol, ViewWithtRes.train == False)).order_by(
                asc(ViewWithtRes.open_time)).all()

            samples = Samples.get_sample_cls(test_candles)
            test_result = samples.create_samples_for_symbol()

            train_candles = db.SESSION.query(ViewWithtRes).filter(
                and_(ViewWithtRes.symbol == symbol, ViewWithtRes.train == True)).order_by(
                asc(ViewWithtRes.open_time)).all()

            samples = Samples.get_sample_cls(train_candles)
            train_candles = samples.create_samples_for_symbol()

            model = ModelNN(train_candles[0], train_candles[1], test_result[0], test_result[1])
            model.model_load()
            model.train_model()
