import config
import datetime
from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime,
    Boolean,
    Float
)
from sqlalchemy.dialects.postgresql import (
    ARRAY
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_string = config.DB_CONN_STRING

db = create_engine(db_string)


class Mixin(object):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    createdAt = Column(DateTime, nullable=False,
                       default=datetime.datetime.utcnow())
    updatedAt = Column(DateTime, nullable=False,
                       default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return f'<{self.__class__.__name__} id="{self.id}">'


base = declarative_base(cls=Mixin)


class Permission(base):
    __tablename__ = 'Permissions'
    name = Column(String(100), nullable=False)


class Country(base):
    __tablename__ = 'Countries'
    name = Column(String, nullable=False)
    alpha2 = Column(String(5), nullable=False)
    alpha3 = Column(String(5), nullable=False)
    flagPath = Column(String, nullable=False)


class City(base):
    __tablename__ = 'Cities'
    name = Column(String, nullable=False)
    country = Column(Integer, ForeignKey(Country.id),
                     nullable=False)


class User(base):
    __tablename__ = 'Users'
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    permission = Column(Integer, ForeignKey(Permission.id), nullable=False)
    fullName = Column(String, nullable=True)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    country = Column(Integer, ForeignKey(Country.id), nullable=False)
    city = Column(Integer, ForeignKey(City.id), nullable=False)
    brandLogoPath = Column(String, nullable=True)
    brandName = Column(String, unique=True, nullable=True)
    brandProductTypes = Column(ARRAY(String), nullable=True)
    active = Column(Boolean, default=False, nullable=False)
    confirmationKey = Column(String, nullable=False, default='con_key')
    confirmed = Column(Boolean, default=False, nullable=False)


class AuthToken(base):
    __tablename__ = 'AuthTokens'
    user = Column(Integer, ForeignKey(User.id), nullable=False)
    token = Column(String, nullable=False)


class Payment(base):
    __tablename__ = 'Payments'
    fromUser = Column(Integer, ForeignKey(User.id), nullable=False)
    toUser = Column(Integer, ForeignKey(User.id), nullable=False)
    amount = Column(Float, nullable=False)

class Report(base):
    __tablename__ = 'Reports'
    reporter = Column(Integer, ForeignKey(User.id), nullable=False)
    header = Column(String, nullable=False)
    body = Column(String, nullable=False)

class Message(base):
    __tablename__ = 'Messages'
    user = Column(Integer, ForeignKey(User.id), nullable=False)
    type = Column(String(4), nullable=False)
    message = Column(String, nullable=False)


class Wallet(base):
    __tablename__ = 'Wallets'
    balance = Column(Float, default=0.0, nullable=False)
    owner = Column(Integer, ForeignKey(User.id), nullable=False)


class OrderInfo(base):
    __tablename__ = 'OrderInfos'
    user = Column(Integer, ForeignKey(User.id))
    address = Column(String, nullable=False)
    city = Column(Integer, ForeignKey(City.id), nullable=False)
    country = Column(Integer, ForeignKey(Country.id), nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)


class Order(base):
    __tablename__ = 'Orders'
    orderedTo = Column(Integer, ForeignKey(User.id), nullable=False)
    orderedBy = Column(Integer, ForeignKey(User.id), nullable=False)
    orderedProduct = Column(String, nullable=False)
    orderText = Column(String, nullable=False)
    info = Column(Integer, ForeignKey(OrderInfo.id), nullable=False)
    done = Column(Boolean, default=False, nullable=False)


class OrderRating(base):
    __tablename__ = 'OrderRatings'
    value = Column(Integer, nullable=False)
    byUser = Column(Integer, ForeignKey(User.id), nullable=False)
    toUser = Column(Integer, ForeignKey(User.id), nullable=False)
    forOrder = Column(Integer, ForeignKey(Order.id), nullable=False)


Session = sessionmaker(db)
session = Session()
base.metadata.create_all(db)
