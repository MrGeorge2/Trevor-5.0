from ...globals.db import DB
from datetime import datetime
from sqlalchemy import Column, Boolean, DATETIME, Integer, String, ForeignKey, and_, Float
from typing import List
from random import sample


class TrainLog(DB.DECLARATIVE_BASE):
    __tablename__ = "TTrainLog"
    id = Column(Integer, primary_key=True)
    create_time = Column(DATETIME)
    loss = Column(Float)
    acc = Column(Float)
    symbol = Column(String)
    note = Column(String)

    @staticmethod
    def add_train_log(loss, acc, symbol, note):
        log = TrainLog(create_time=datetime.now(), loss=loss, acc=acc, symbol=symbol, note=note)
        DB.SESSION.add(log)
        DB.SESSION.commit()
