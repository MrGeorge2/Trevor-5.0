from ..globals.config import Config
import os
import numpy as np
from tensorflow.keras.models import load_model, Sequential
from ..data_analysis.models.train_log import TrainLog
from tensorflow.keras.layers import Dense, LSTM, Dropout, Flatten, BatchNormalization
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.callbacks import TensorBoard
from datetime import datetime


class ModelNN:
    def __init__(self):
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []
        self.name = f"LSTM test {datetime.now()}"
        self.tensorboard = TensorBoard(log_dir=f'logs./{self.name}')

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
        model.add(LSTM(units=128, return_sequences=True, input_shape=(Config.TIMESTEPS, Config.FINAL_SAMPLE_COLUMNS)))
        # model.add(BatchNormalization())

        for i in range(8):
            model.add(LSTM(units=64, return_sequences=True))
            # model.add(BatchNormalization())

        model.add(LSTM(units=32, return_sequences=False))
        # model.add(BatchNormalization())

        model.add(Dense(units=8, activation="relu"))
        model.add(Dense(units=4, activation="relu"))
        model.add(Dense(units=1, activation='sigmoid'))
        opt = SGD()
        model.compile(optimizer=opt, loss='binary_crossentropy', metrics=["accuracy"])
        self.model = model
        print("Model created.")
        self.save()

    def train(self):
        self.model.fit(
            self.x_train,
            self.y_train,
            epochs=Config.EPOCHS,
            batch_size=64,
            validation_data=(self.x_test, self.y_test),
            verbose=1
        )
        self.save()

    def eval(self, symbol, note):
        score = self.model.evaluate(self.x_test, self.y_test, verbose=1)
        loss = score[0]
        acc = score[1]

        TrainLog.add_train_log(loss=loss, acc=acc, symbol=symbol, note=note)
        print(f'Test loss: {score[0]} / Test accuracy: {score[1]}')
        self.x_test = []
        self.y_test = []
        self.save()
    
    def show_real_output(self):
        for i in range(50):
            test_sample = self.x_test[i:i+1, :, :]
            print(f"TEST: predicted: {self.model.predict(test_sample)},  real: {self.y_test[i, :]}")
        for i in range(50):
            train_sample = self.x_train[i:i+1, :, :]
            print(f"TRAIN: predicted: {self.model.predict(train_sample)},  real: {self.y_train[i, :]}")


