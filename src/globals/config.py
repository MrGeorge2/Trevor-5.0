from decimal import *
from binance.client import Client


class Config:
    TIMESTEPS = 60

    SYMBOL = "BTC/USDT"
    DEBUGING = True
    MARGIN_TRADING = False
    EMULATION = True
    PLOTING = False
    BACKTESTING_DATA = False
    STORE_BACK_TEST_DATA = False
    MINIMAL_DELTA = 0
    """
    LIVE TRADING
    """
    SIMULATION = True
    SYMBOL_LIVE_TRADING = [
            "BTCUSDT",
    ]
    SL: Decimal = Decimal(0.17)  # %
    TP: Decimal = Decimal(0.17)  # %

    FEE: Decimal = Decimal(0.036)     # %

    """
    SCRAPER
    """
    CANDLE_INTERVAL = 900   # v sekundach 900 s = 15 minut
    CANDLE_MINUTES_INTERVAL = 12
    CHECK_ROW_IN_DB = False

    SYMBOLS_TO_SCRAPE = [
        #  --- USDT ---
        "BTCUSDT",
        "ETHUSDT",
        "LTCUSDT",
        "XMRUSDT",
        "LINKUSDT",
        "YFIUSDT",
        "MKRUSDT",
        "AAVEUSDT",
        "COMPUSDT",
        "DASHUSDT",
        "BNBUSDT",
        "ZECUSDT",
    ]

    SYMBOL_GROUPS_1H = [
        "BTCUSDT",
        "ETHUSDT",
        "LTCUSDT",
        "XMRUSDT",
        "LINKUSDT",
        "YFIUSDT",
        "MKRUSDT",
        "AAVEUSDT",
        "COMPUSDT",
        "DASHUSDT",
        "BNBUSDT",
        "ZECUSDT",
    ]

    """
    #### ORDERS ####
    """
    ACCOUNT_CAPITAL_SIMULATION = 0.007
    BTC = 220000
    PERCENT_OF_CAPITAL_TO_TRADE = Decimal(1)  # 0.03
    BALANCE_TO_TRADE = Decimal(0.001)  # s kolika BTC obchodovat

    """
    Order
    """
    # V jednotkach preccission
    SL_HIGHER_LIMIT_PRECESSION = 20
    SL_TRIGGER = 2
    TP_HIGHER_LIMIT_PRECISSION = 2

    """
    #### API HANDLER ####
    """
    API_KEY = "LXru2T0wR2zilayCA3vKBDkYmh12b2NgHfM583Zd"
    S_KEY = "3yv71kxXuvtXlXJVdYFEGPCewSayVq3lT-AESWuy"
    TIMEOUT = 20

    """
    ### SAMPLES ###
    """
    RANDOM_SYMBOLS_FOR_SAMPLE = 5
    NUMBER_OF_SAMPLE_COLUMNS = 92
    FINAL_SAMPLE_COLUMNS = 9
    NUMBER_FUTURE_CANDLE_PREDICT = 4

    """
    #### MODEL ####
    """
    PATH_MODEL = "./src/nn_model/data/model.h5"
    EPOCHS = 10
    EPOCHS_ITERATION = 30

    """
    #### TRAIN TWO SAMPLES ####
    """
    # pro testovani modelu na par vzorcich, jestli se pretrenuje
    NUMBER_OF_SAMPLES_FOR_NN_TEST = 2

