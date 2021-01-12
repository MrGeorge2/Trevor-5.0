from ..globals.config import Config
import os
import numpy as np
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.optimizers import Adam



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
        model = Sequential()
        model.add(LSTM(units=64, return_sequences=True, input_shape=(Config.TIMESTEPS, Config.FINAL_SAMPLE_COLUMNS)))

        model.add(LSTM(units=64, return_sequences=True))

        model.add(LSTM(units=32, return_sequences=True))
        model.add(LSTM(units=32, return_sequences=True))

        model.add(LSTM(units=32, return_sequences=False))

        model.add(Dense(units=32, activation="relu"))
        model.add(Dense(units=16, activation="relu"))
        model.add(Dense(units=8, activation="relu"))

        model.add(Dense(units=2, activation="relu"))
        model.add(Dense(units=1, activation='sigmoid'))
        opt = Adam(learning_rate=0.00005)
        model.compile(optimizer=opt, loss='binary_crossentropy', metrics=["binary_accuracy"])
        self.model = model
        print("Model created.")
        self.save()

    def train(self):
        self.model.fit(self.x_train, self.y_train, epochs=Config.EPOCHS, batch_size=32, validation_data=(self.x_test, self.y_test))
        self.save()
    
    def show_real_output(self):
        for i in range(100):
            sample = self.x_test[i:i+1, :, :]
            print(f"predicted: {self.model.predict(sample)}, argmax: {np.argmax(self.model.predict(sample))},  real: {self.y_test[i, :]}")
