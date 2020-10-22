from sqlalchemy import text
from ...db import *

def permissions_get(sql=""):
    q = session.query(Permission)
    if not sql == "":
        q = session.query(Permission).filter(text(sql))
    l = q.all()
    return {
        "body": l,
        "query": q
    }


def countries_get(sql=""):
    q = session.query(Country)
    if not sql == "":
        q = session.query(Country).filter(text(sql))
    l = q.all()
    return {
        "body": l,
        "query": q
    }


def cities_get(sql=""):
    q = session.query(City)
    if not sql == "":
        q = session.query(City).filter(text(sql))
    l = q.all()
    return {
        "body": l,
        "query": q
    }


def users_get(sql=""):
    q = session.query(User)
    if not sql == "":
        q = session.query(User).filter(text(sql))
    l = q.all()
    return {
        "body": l,
        "query": q
    }


def authtokens_get(sql=""):
    q = session.query(AuthToken)
    if not sql == "":
        q = session.query(AuthToken).filter(text(sql))
    l = q.all()
    return {
        "body": l,
        "query": q
    }


def payments_get(sql=""):
    q = session.query(Payment)
    if not sql == "":
        q = session.query(Payment).filter(text(sql))
    l = q.all()
    return {
        "body": l,
        "query": q
    }


def reports_get(sql=""):
    q = session.query(Report)
    if not sql == "":
        q = session.query(Report).filter(text(sql))
    l = q.all()
    return {
        "body": l,
        "query": q
    }


def messages_get(sql=""):
    q = session.query(Message)
    if not sql == "":
        q = session.query(Message).filter(text(sql))
    l = q.all()
    return {
        "body": l,
        "query": q
    }


def wallets_get(sql=""):
    q = session.query(Wallet)
    if not sql == "":
        q = session.query(Wallet).filter(text(sql))
    l = q.all()
    return {
        "body": l,
        "query": q
    }


def orderinfos_get(sql=""):
    q = session.query(OrderInfo)
    if not sql == "":
        q = session.query(OrderInfo).filter(text(sql))
    l = q.all()
    return {
        "body": l,
        "query": q
    }


def orders_get(sql=""):
    q = session.query(Order)
    if not sql == "":
        q = session.query(Order).filter(text(sql))
    l = q.all()
    return {
        "body": l,
        "query": q
    }


def orderratings_get(sql=""):
    q = session.query(OrderRating)
    if not sql == "":
        q = session.query(OrderRating).filter(text(sql))
    l = q.all()
    return {
        "body": l,
        "query": q
    }
