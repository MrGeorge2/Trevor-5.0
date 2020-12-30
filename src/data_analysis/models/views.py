from ...globals.db import DB
from sqlalchemy import Table, Column, Integer



db = DB.get_globals()


class ViewWithoutRes(db.DECLARATIVE_BASE):
    __table__ = Table("VJoined", db.DECLARATIVE_BASE.metadata,
                      Column("id", Integer, primary_key=True),
                             autoload=True, autoload_with=db.ENGINE
                    )


class ViewWithtRes(DB.DECLARATIVE_BASE):
    __table__ = Table("VJoinedVRes", DB.DECLARATIVE_BASE.metadata,
                      Column("id", Integer, primary_key=True),
                      autoload=True, autoload_with=db.ENGINE,
                    )


