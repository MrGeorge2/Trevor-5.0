from config import Config
class Model:

    def __init__(self):
        self.cfg = Config()

        self.x = None
        self.x_train = None

        self.x_test = None
        self.y_train = None
        self.y_test = None

        self.load_dataset()
        self.model = self.nacteni_modelu()

        self.vypis_unique()

    def load_dataset(self):
         # TODO: nastavit podle zpusobu zpracovani vzorku
         # self.x_train self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=0.2, random_state=0)
        pass

    def vypis_unique(self):
        print(f"rozlozeni kategorii v datasetu")
        unique, counts = np.unique(self.y, return_counts=True)
        print(dict(zip(unique, counts)))

    def nacteni_modelu(self):
        if os.path.exists(self.cfg.PATH_MODEL):
            load_model(self.cfg.PATH_MODEL)
            return self.model
        else:
            self.create_model()
            self.nacteni_modelu()

    def create_model(self):
        self.model = Sequential()
        self.model.add(LSTM(units=128, return_sequences=True, input_shape=(np.shape(self.X_train)[1:])))
        self.model.add(Dropout(0.1))
        self.model.add(LSTM(units=64, return_sequences=True))
        self.model.add(Dropout(0.1))
        self.model.add(LSTM(units=64, return_sequences=True))
        self.model.add(Dropout(0.1))
        self.model.add(LSTM(units=64, return_sequences=False))
        self.model.add(Dropout(0.1))

        self.model.add(Dense(units=64, activation="relu"))
        self.model.add(Dropout(0.1))
        self.model.add(Dense(units=64, activation="relu"))
        self.model.add(Dropout(0.1))
        self.model.add(Dense(units=32, activation="relu"))
        self.model.add(Dropout(0.1))
        self.model.add(Dense(units=16, activation="relu"))
        self.model.add(Dropout(0.1))

        self.model.add(Dense(units=2, init='uniform', activation='softmax'))

        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=["accuracy"])

        self.model.save(self.cfg.PATH_MODEL)

    def train_model(self):
        for i in range(self.cfg.EPOCHS):
            self.model.fit(self.x_train self.y_train, epochs=1, batch_size=64, validation_data=(self.x_test, self.y_test))
            print(f"epoch : {i}")
        self.model.save(self.cfg.PATH_MODEL)

        if __name__ == "__main__":
            model = Model()