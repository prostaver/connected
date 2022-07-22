from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("postgresql://billy:endoftheworld@192.168.0.115:5432/classified", echo=True)

Base = declarative_base()

DbSession = sessionmaker(bind=engine)

def getDbConection():
    db = DbSession()
    try:
        yield db
    finally:
        db.close()