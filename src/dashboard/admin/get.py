import sqlite3
from ...schema import *


def permissions_get(sql=""):
    query = 'SELECT * FROM Permissions'
    if not sql == "":
        query += f' WHERE {sql}'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(query)
    l = c.fetchall()
    l = list(map(lambda x: Permission(x), l))
    return {
        "body": l,
        "rows": len(l),
        "query": query
    }


def countries_get(sql=""):
    query = 'SELECT * FROM Countries'
    if not sql == "":
        query += f' WHERE {sql}'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(query)
    l = c.fetchall()
    l = list(map(lambda x: Country(x), l))
    return {
        "body": l,
        "query": query
    }


def cities_get(sql=""):
    query = 'SELECT * FROM Cities'
    if not sql == "":
        query += f' WHERE {sql}'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(query)
    l = c.fetchall()
    l = list(map(lambda x: City(x, convert='*'), l))
    return {
        "body": l,
        "query": query
    }


def users_get(sql=""):
    query = 'SELECT * FROM Users'
    if not sql == "":
        query += f' WHERE {sql}'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(query)
    l = c.fetchall()
    l = list(map(lambda x: User(x, convert='*'), l))
    return {
        "body": l,
        "query": query
    }


def authtokens_get(sql=""):
    query = 'SELECT * FROM AuthTokens'
    if not sql == "":
        query += f' WHERE {sql}'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(query)
    l = c.fetchall()
    l = list(map(lambda x: AuthToken(x, convert='*'), l))
    return {
        "body": l,
        "query": query
    }


def payments_get(sql=""):
    query = 'SELECT * FROM Payments'
    if not sql == "":
        query += f' WHERE {sql}'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(query)
    l = c.fetchall()
    l = list(map(lambda x: Payment(x, convert='*'), l))
    return {
        "body": l,
        "query": query
    }


def reports_get(sql=""):
    query = 'SELECT * FROM Reports'
    if not sql == "":
        query += f' WHERE {sql}'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(query)
    l = c.fetchall()
    l = list(map(lambda x: Report(x, convert='*'), l))
    return {
        "body": l,
        "query": query
    }


def messages_get(sql=""):
    query = 'SELECT * FROM Messages'
    if not sql == "":
        query += f' WHERE {sql}'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(query)
    l = c.fetchall()
    l = list(map(lambda x: Message(x, convert='*'), l))
    return {
        "body": l,
        "query": query
    }


def wallets_get(sql=""):
    query = 'SELECT * FROM Wallets'
    if not sql == "":
        query += f' WHERE {sql}'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(query)
    l = c.fetchall()
    l = list(map(lambda x: Wallet(x, convert='*'), l))
    return {
        "body": l,
        "query": query
    }


def orderinfos_get(sql=""):
    query = 'SELECT * FROM OrderInfos'
    if not sql == "":
        query += f' WHERE {sql}'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(query)
    l = c.fetchall()
    l = list(map(lambda x: OrderInfo(x, convert='*'), l))
    return {
        "body": l,
        "query": query
    }


def orders_get(sql=""):
    query = 'SELECT * FROM Orders'
    if not sql == "":
        query += f' WHERE {sql}'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(query)
    l = c.fetchall()
    l = list(map(lambda x: Order(x, convert='*'), l))
    return {
        "body": l,
        "query": query
    }


def orderratings_get(sql=""):
    query = 'SELECT * FROM OrderRatings'
    if not sql == "":
        query += f' WHERE {sql}'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(query)
    l = c.fetchall()
    l = list(map(lambda x: OrderRating(x, convert='*'), l))
    return {
        "body": l,
        "query": query
    }
