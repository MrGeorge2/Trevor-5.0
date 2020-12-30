from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session


class DB:
    ENGINE = None
    SESSION: Session = None
    DECLARATIVE_BASE = declarative_base()

    def __init__(self):
        self.__init_db()

    @classmethod
    def __init_db(cls):
        cls.ENGINE = create_engine('sqlite:///trevor.db', echo=True)
        # cls.DECLARATIVE_BASE = declarative_base(bind=cls.ENGINE)
        cls.DECLARATIVE_BASE.metadata.create_all(cls.ENGINE)
        sess = sessionmaker(bind=cls.ENGINE)
        sess.configure(bind=cls.ENGINE)

        cls.SESSION = sess()

    @classmethod
    def get_globals(cls):
        return DB()
