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
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.orm import sessionmaker, validates

import re
from .validators import email_validation, phone_num_validation

db_string = config.DB_CONN_STRING
engine = create_engine(db_string)


class MutableList(Mutable, list):
    def append(self, value):
        list.append(self, value)
        self.changed()

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value


class Mixin(object):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    createdAt = Column(DateTime, nullable=False,
                       default=datetime.datetime.utcnow())
    updatedAt = Column(DateTime, nullable=False,
                       default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}>'


Base = declarative_base(cls=Mixin)


class Permission(Base):
    __tablename__ = 'Permissions'
    name = Column(String(100), nullable=False)


class Country(Base):
    __tablename__ = 'Countries'
    name = Column(String, nullable=False)
    alpha2 = Column(String(5), nullable=False)
    alpha3 = Column(String(5), nullable=False)
    flagPath = Column(String, nullable=False)
    phonePrefix = Column(Integer, nullable=True, default=0)


class City(Base):
    __tablename__ = 'Cities'
    name = Column(String, nullable=False)
    country = Column(Integer, ForeignKey(Country.id),
                     nullable=False)


class User(Base):
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
    brandNameSynonyms = Column(ARRAY(String), nullable=True)
    brandProductTypes = Column(
        MutableList.as_mutable(ARRAY(String)), nullable=True)
    active = Column(Boolean, default=True, nullable=False)
    confirmationKey = Column(String, nullable=False, default='con_key')
    confirmed = Column(Boolean, default=False, nullable=False)

    @validates('username')
    def validate_username(self, key, username):
        if not 3 <= len(username) <= 25:
            raise ValueError(
                'Username should be longer than 3 characters and shorter than 25')
        return username

    @validates('password')
    def validate_password(self, key, password):
        from ..account.security import hashPassword
        if not 8 <= len(password):
            raise ValueError('Password should be at least 8 characters')
        if not re.search(r'[A-Z]', password):
            raise ValueError(
                'Password should contain at least 1 uppercase character')
        if not re.search(r'[a-z]', password):
            raise ValueError(
                'Password should contain at least 1 lowercase character')
        if not re.search(r'[0-9]', password):
            raise ValueError('Password should contain at least 1 digit')
        return hashPassword(password)

    @validates('email')
    def validate_email(self, key, email):
        if not email_validation(email):
            raise ValueError('Please enter valid email')
        return email

    @validates('phone')
    def validate_phone(self, key, phone):
        if not phone_num_validation(phone):
            raise ValueError(
                'Please enter international version of a real phone number')
        return phone


class PasswordRecover(Base):
    __tablename__ = 'PasswordRecover'
    user = Column(ForeignKey(User.id), nullable=False)
    token = Column(String, nullable=False)
    active = Column(Boolean, default=True)


class AuthToken(Base):
    __tablename__ = 'AuthTokens'
    user = Column(Integer, ForeignKey(User.id), nullable=False)
    token = Column(String, nullable=False)


class Payment(Base):
    __tablename__ = 'Payments'
    fromUser = Column(Integer, ForeignKey(User.id), nullable=False)
    toUser = Column(Integer, ForeignKey(User.id), nullable=False)
    amount = Column(Float, nullable=False)


class Report(Base):
    __tablename__ = 'Reports'
    reporter = Column(Integer, ForeignKey(User.id), nullable=False)
    header = Column(String, nullable=False)
    body = Column(String, nullable=False)


class Message(Base):
    __tablename__ = 'Messages'
    user = Column(Integer, ForeignKey(User.id), nullable=False)
    type = Column(String(4), nullable=False)
    message = Column(String, nullable=False)


class Wallet(Base):
    __tablename__ = 'Wallets'
    balance = Column(Float, default=0.0, nullable=False)
    owner = Column(Integer, ForeignKey(User.id), nullable=False)


class Order(Base):
    __tablename__ = 'Orders'
    orderedTo = Column(Integer, ForeignKey(User.id), nullable=False)
    orderedBy = Column(Integer, ForeignKey(User.id), nullable=False)
    orderedProduct = Column(String, nullable=False)
    orderText = Column(String, nullable=False)
    comments = Column(String, nullable=True, default='')
    done = Column(Boolean, default=False, nullable=False)


class ServerError(Base):
    __tablename__ = 'ServerErrors'
    where = Column(String, nullable=False)
    errorCode = Column(Integer, nullable=False)
    errorDesc = Column(String, nullable=False)
    fixed = Column(Boolean, nullable=False, default=False)


Session = sessionmaker(engine)
session = Session()
# Base.metadata.create_all(engine)
