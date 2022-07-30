import configparser
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

config = configparser.ConfigParser()

config.read(os.path.dirname(os.path.abspath(__file__))+"/config.ini")
config.sections()

dbConfig = config['DATABASE']
dbEngine = dbConfig["ENGINE"]
dbUser = dbConfig["USER"]
dbPW = dbConfig["PASSWORD"]
dbHost = dbConfig["HOST"]
dbPort = dbConfig["PORT"]
dbName = dbConfig["DBNAME"]

engine = create_engine(f"{dbEngine}://{dbUser}:{dbPW}@{dbHost}:{dbPort}/{dbName}", echo=True)

Base = declarative_base()

DbSession = sessionmaker(bind=engine)

def get_db_connection():
    db = DbSession()
    try:
        yield db
    finally:
        db.close()