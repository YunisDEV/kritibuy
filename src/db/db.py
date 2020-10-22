import config
from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    String,
    Integer,
    VARCHAR
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_string = config.DB_CONN_STRING

db = create_engine(db_string)

base = declarative_base()


class Permission(base):
    __tablename__ = 'Permissions'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(VARCHAR(length=100), nullable=False)


class Country(base):
    __tablename__ = 'Countries'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    alpha2 = Column(VARCHAR(5), nullable=False)
    alpha3 = Column(VARCHAR(5), nullable=False)
    flagPath = Column(String, nullable=False)


class City(base):
    __tablename__ = 'Cities'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    country = Column(Integer, nullable=False) # FOREIGN KEY Countries(id)


Session = sessionmaker(db)
session = Session()
base.metadata.create_all(db)
