from ..globals.config import Config
import os
import numpy as np
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout


class ModelNN:
    def __init__(self):
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []

        self.model = self.load()

    def set_train_samples(self, train_samples):
        self.x_train = train_samples[0]
        self.y_train = train_samples[1]

    def set_test_samples(self, test_samples):
        self.x_test = test_samples[0]
        self.y_test = test_samples[1]

    def print_unique(self):
        unique, counts = np.unique(self.y_train, return_counts=True)
        print(f"Četnosti kategorií v tréninkovém datasetu: {dict(zip(unique, counts))}")

    def load(self):
        if os.path.isfile(Config.PATH_MODEL):
            model = load_model(Config.PATH_MODEL)
            print("Model loaded.")
            return model
        else:
            self.create()
            self.model = self.load()

    def save(self):
        self.model.save(Config.PATH_MODEL)
        print("Model saved.")

    def create(self):
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

        self.model.add(Dense(units=1, activation='sigmoid'))
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=["categorical_accuracy"])
        print("Model created.")
        self.save()

    def train(self):
        self.model.fit(self.x_train, self.y_train, epochs=Config.EPOCHS, batch_size=32, validation_data=(self.x_test, self.y_test))
        self.save()
    
    def show_real_output(self):
        for i in range(100):
            print(f"predicted: {self.model.predict(self.x_test[i, :, :])},  real: {self.y_test[i, :]}")
