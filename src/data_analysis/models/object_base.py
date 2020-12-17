from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///trevor.db', echo=True)

class ObjectBase(Base):
    __tablename__ = 'TBase'

    id = Column(Integer, primary_key=True)