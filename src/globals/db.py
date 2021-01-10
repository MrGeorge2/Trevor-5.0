from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session
import os


class DB:
    ENGINE = None
    SESSION: Session = None
    DECLARATIVE_BASE = declarative_base()
    SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "\\sql_scripts\\")

    def __init__(self):
        self.__init_db()

    @classmethod
    def __init_db(cls):
        cls.ENGINE = create_engine('sqlite:///trevor.db', echo=False, connect_args={'check_same_thread': False})
        # cls.DECLARATIVE_BASE = declarative_base(bind=cls.ENGINE)
        cls.DECLARATIVE_BASE.metadata.create_all(cls.ENGINE)

        sess = sessionmaker(bind=cls.ENGINE)
        sess.configure(bind=cls.ENGINE)

        cls.SESSION = sess()

        cls.execute_sql("view_joined_with_res.sql")
        cls.execute_sql("view_joined_without_res.sql")

    @classmethod
    def execute_sql(cls, script_name: str):
        sql_file = open(DB.create_scripts_path(script_name))
        sql_command = ''

        # Iterate over all lines in the sql file
        for line in sql_file:
            # Ignore commented lines
            if not line.startswith('--'):
                # Append line to the command string
                sql_command += line
                sql_command = sql_command.replace("\t", " ")
                sql_command = sql_command.replace("\n", " ")

                # If the command string ends with ';', it is a full statement
                if sql_command.endswith(';'):
                    # Try to execute statement and commit it
                    try:
                        cls.SESSION.execute(text(sql_command))
                        cls.SESSION.commit()

                    # Assert in case of error
                    except Exception as e:
                        raise Exception(e)

                    # Finally, clear command string
                    finally:
                        sql_command = ''

    @staticmethod
    def create_scripts_path(script_name: str):
        dir: str = os.path.dirname(__file__)
        splitted_dir = dir.split('\\')
        src_path_splitted = splitted_dir[:-1]
        src_path_splitted.append("sql_scripts")
        src_path = "\\".join(src_path_splitted)
        return os.path.join(src_path, script_name)



    @classmethod
    def get_globals(cls):
        return DB()
