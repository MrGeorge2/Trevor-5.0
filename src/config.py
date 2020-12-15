from decimal import *
import os


class Config:
    TIMESTEPS = 200

    DEBUGING = True
    MARGIN_TRADING = False
    EMULATION = True
    PLOTING = False
    BACKTESTING_DATA = False
    STORE_BACK_TEST_DATA = False

    DATA_FILE_NAME = os.path.normpath(os.path.join(os.path.dirname(__file__), 'data/data1'))  # #NESAHAT!
    DATA_FILE_NAME_TEMPLATE = os.path.normpath(os.path.join(os.path.dirname(__file__), 'data/data'))  # #NESAHAT!

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

    FILE_NUM = 1

    """
    #### MODEL ####
    """
    PATH_MODEL = "./nn_model/data/model.h5"
    EPOCHS = 50