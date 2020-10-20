import sqlite3
from ..schema import *
from flask import make_response


def permissions(sql=""):
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


def permissions_post(request):
    resp = make_response()
    return resp


def countries(sql=""):
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


def cities(sql=""):
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


def users(sql=""):
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


def authtokens(sql=""):
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


def payments(sql=""):
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


def reports(sql=""):
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


def messages(sql=""):
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


def wallets(sql=""):
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
def orders(sql=""):
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
def orderrating(sql=""):
    query = 'SELECT * FROM OrderRating'
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
db_data_get = {
    "Permissions": permissions,
    "Countries": countries,
    "Cities": cities,
    "Users": users,
    "AuthTokens": authtokens,
    "Payments": payments,
    "Reports": reports,
    "Messages": messages,
    "Wallets": wallets,
    "Orders": orders,
    "OrderRating": orderrating
}

db_data_post = {
    "Permissions": ''
}
