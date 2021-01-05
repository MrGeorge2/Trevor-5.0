from ..globals.config import Config
import os
import numpy as np
from keras.models import load_model, Sequential
from keras.layers import Dense, LSTM, Dropout


class ModelNN:
    def __init__(self, x_train, y_train, x_test, y_test):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test

        self.model = self.nacteni_modelu()
        self.vypis_unique()

    def vypis_unique(self):
        unique, counts = np.unique(self.y_train, return_counts=True)
        print(f"Četnosti kategorií v tréninkovém datasetu: {dict(zip(unique, counts))}")

    def nacteni_modelu(self):
        if os.path.exists(Config.PATH_MODEL):
            model = load_model(Config.PATH_MODEL)
            return model
        else:
            self.create_model()
            self.nacteni_modelu()

    def create_model(self):
        self.model = Sequential()
        self.model.add(LSTM(units=128, return_sequences=True, input_shape=(np.shape(self.x_train)[1:])))
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
        self.model.save(Config.PATH_MODEL)

    def train_model(self):
        self.model.fit(self.x_train, self.y_train, epochs=Config.EPOCHS, batch_size=64, validation_data=(self.x_test, self.y_test))
        self.model.save(Config.PATH_MODEL)
