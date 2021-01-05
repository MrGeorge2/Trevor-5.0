from decimal import *
import os


class Config:
    TIMESTEPS = 100

    DEBUGING = True
    MARGIN_TRADING = False
    EMULATION = True
    PLOTING = False
    BACKTESTING_DATA = False
    STORE_BACK_TEST_DATA = False
    """
    SCRAPER
    """
    CHECK_ROW_IN_DB = False
    SYMBOLS_TO_SCRAPE = [
        #  --- USDT ---
        "BTCUSDT",
        "ETHUSDT",
        "XRPUSDT",
        "LTCUSDT",
        "BCHUSDT",
        "EOSUSDT",
        "ADAUSDT",
        "DOTUSDT",
        "LINKUSDT",
        "TRXUSDT",
        "BNBUSDT",
        "XLMUSDT",
        "XMRUSDT",
        "UNIUSDT",
        "ETCUSDT",
        "DASHUSDT",
        "VETUSDT",
        "ATOMUSDT",
        "QTUMUSDT",
        "DAIUSDT",
        "XTZUSDT",
        "FILUSDT",
        "RENUSDT",
        "AAVEUSDT",
        "COMPUSDT",
        "BATUSDT",
        "XEMUSDT",
        "ONTUSDT",
        "DOGEUSDT",

        # --- BTC ---
        "XRPBTC",
        "ETHBTC",
        "REEFBTC",
        "ADABTC",
        "DOTBTC",
        "BNBBTC",
        "LINKBTC",
        "LTCBTC",
        "BCHBTC",
        "RENBTC",
        "THETABTC",
        "XMRBTC",
        "YFIBTC",
        "UNFIBTC",
        "WAVESBTC",
        "ATOMBTC",
        "ALGOBTC",
        "INJBTC",
        "NEOBTC",
        "KSMBTC",
        "RUNEBTC",
        "DASHBTC",
        "LUNABTC",
        "UNIBTC",
        "ZENBTC",
        "FILBTC",
        "OCEANBTC",

        # --- ETH ---
        "XRPETH",
        "BNBETH",
        "VETETH",
        "LTCETH",
        "LINKETH",
        "GRTETH",
        "ZILETH",
        "THETAETH",
        "XEMETH",
        "XLMETH",
        "EOSETH",
        "XMRETH",
        "AAVEETH",
        "HOTETH",
        "ENJETH",
        "DASHETH",
        "EASYETH",
        "OMGETH",
        "NEOETH",
        "LRCETH",
        "NASETH",
        "ZECETH",
        "WANETH",

        # --- BNB ---
        "XRPBNB",
        "ADABNB",
        "DOTBNB",
        "LTCBNB",
        "EOSBNB",
        "BCHBNB",
        "MKRBNB",
        "KP3RBNB",
        "XMRBNB",
        "YFIBNB",
        "YFIIBNB",
        "AAVEBNB",
        "ZECBNB",
        "KSMBNB",
        "DASHBNB"
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
    NUMBER_OF_SAMPLE_COLUMNS = 16
    FINAL_SAMPLE_COLUMNS = 14

    """
    #### MODEL ####
    """
    PATH_MODEL = "./src/nn_model/data/model.h5"
    EPOCHS = 5
