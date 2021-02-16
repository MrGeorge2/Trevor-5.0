from ..globals.config import Config
import os
import numpy as np
from tensorflow.keras.regularizers import l1_l2
from tensorflow.keras.models import load_model, Sequential
from ..data_analysis.models.train_log import TrainLog
from tensorflow.keras.layers import Dense, LSTM, Dropout, Flatten, BatchNormalization, Bidirectional, TimeDistributed
from tensorflow.keras.optimizers import Adam, SGD, Adadelta
from tensorflow.keras.callbacks import TensorBoard
from datetime import datetime
import os


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
        model.add(LSTM(units=128, return_sequences=True, input_shape=(Config.TIMESTEPS, Config.FINAL_SAMPLE_COLUMNS),))
        model.add(Dropout(0.2))
        model.add(BatchNormalization())

        model.add((LSTM(units=128, return_sequences=True)))
        model.add(Dropout(0.2))
        model.add(BatchNormalization())

        model.add(LSTM(units=128, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(BatchNormalization())

        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.2))

        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.2))

        model.add(Dense(32, activation='relu'))
        model.add(Dropout(0.2))

        model.add(Dense(8, activation='relu'))
        model.add(Dropout(0.2))

        model.add(Dense(units=2, activation='relu'))
        opt = Adam(learning_rate=0.001, decay=1e-6)
        model.compile(optimizer=opt, loss='mean_squared_error', metrics=['accuracy'])
        self.model = model
        print("Model created.")
        self.model.build(input_shape=(None, Config.TIMESTEPS, Config.FINAL_SAMPLE_COLUMNS))
        self.save()

    def train(self):
        self.model.fit(
            self.x_train,
            self.y_train,
            epochs=Config.EPOCHS,
            batch_size=128,
            validation_data=(self.x_test, self.y_test),
            verbose=1,
            shuffle=True,
        )
        self.save()

    def predict(self, input_data):
        predicted = self.model.predict(input_data)
        return predicted[0, 0], predicted[0, 1]

    def eval(self, symbol, note):
        score = self.model.evaluate(self.x_test, self.y_test, verbose=1)
        loss = score[0]
        acc = score[1]

        os.system(f'cmd /c "git commit -am "model checkpoint loss={loss} acc={acc} note={note}"')
        TrainLog.add_train_log(loss=loss, acc=acc, symbol=symbol, note=note)
        print(f'Test loss: {score[0]} / Test accuracy: {score[1]}')
        self.x_test = []
        self.y_test = []
        self.save()
    
    def show_real_output(self):
        for i in range(50):
            test_sample = self.x_test[i:i+1, :, :]
            real = self.y_test[i]
            print(f"TEST: predicted: {self.model.predict(test_sample)},  real: {real}")
        for i in range(50):
            train_sample = self.x_train[i:i+1, :, :]
            real = self.y_train[i]
            print(f"TRAIN: predicted: {self.model.predict(train_sample)},  real: {real}")


