from decimal import *
from binance.client import Client


class Config:
    TIMESTEPS = 60

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
    CANDLE_INTERVAL = Client.KLINE_INTERVAL_15MINUTE
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
    API_KEY = "4ccjv0lPKB4CTJf4p4EGbs3N1zvbNpFs2f6GNHHxv4DggoJ2eF4lO4Ee6E6xmOxI"
    S_KEY = "RjV0u0Psrk5SPefQtWAEIcVUeXkoVWcpY5CgZEtyENRfMjPajK37t1Evq4fDwTd0"
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

