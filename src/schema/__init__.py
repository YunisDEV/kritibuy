import sqlite3
import datetime
import json

def date(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')


class Permission:
    def __init__(self, data):
        self.id = int(data[0])
        self.name = str(data[1])


class Country:
    def __init__(self, data):
        self.id = int(data[0])
        self.name = str(data[1])
        self.alpha2 = str(data[2])
        self.alpha3 = str(data[3])
        self.flagPath = str(data[4])


class City:
    def __init__(self, data, convert=[]):
        self.id = int(data[0])
        self.name = str(data[1])
        self.country = int(data[2])

        if 'country' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Countries WHERE id={self.country}""")
            self.Country = Country(c.fetchone())


class User:
    def __init__(self, data, convert=[]):
        self.id = int(data[0])
        self.username = str(data[1])
        self.password = str(data[2])
        self.email = str(data[3])
        self.permission = int(data[4])
        self.fullName = str(data[5])
        self.address = str(data[6])
        self.phone = str(data[7])
        self.country = int(data[8])
        self.city = int(data[9])
        self.brandLogoPath = str(data[10])
        self.brandName = str(data[11])
        self.createdAt = date(data[12])
        self.brandProductTypes = str(data[13])
        self.active = bool(data[14])
        self.confirmationKey = str(data[15])
        self.confirmed = bool(data[16])

        if 'permission' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(
                f"""SELECT * FROM Permissions WHERE id={self.permission}""")
            self.Permission = Permission(c.fetchone())

        if 'country' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(
                f"""SELECT * FROM Countries WHERE id={self.country}""")
            self.Country = Country(c.fetchone())

        if 'city' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(
                f"""SELECT * FROM Cities WHERE id={self.city}""")
            self.City = City(c.fetchone())

        if 'brandProductTypes' in convert or convert == "*":
            self.BrandProductTypes = tuple(json.loads(self.brandProductTypes))

class AuthToken:
    def __init__(self, data, convert=[]):
        self.id = int(data[0])
        self.user = int(data[1])
        self.token = str(data[2])

        if 'user' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(
                f"""SELECT * FROM Users WHERE id={self.user}""")
            self.User = User(c.fetchone())


class Payment:
    def __init__(self, data, convert=[]):
        self.id = int(data[0])
        self.fromUser = int(data[1])
        self.toUser = int(data[2])
        self.amount = float(data[3])
        self.date = date(data[3])

        if 'user' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Users WHERE id={self.fromUser}""")
            self.FromUser = User(c.fetchone())
            c.execute(f"""SELECT * FROM Users WHERE id={self.toUser}""")
            self.ToUser = User(c.fetchone())


class Report:
    def __init__(self, data, convert=[]):
        self.id = int(data[0])
        self.reporter = int(data[1])
        self.header = str(data[2])
        self.body = str(data[3])
        self.date = date(data[4])

        if 'user' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Users WHERE id={self.reporter}""")
            self.Reporter = User(c.fetchone())


class Message:
    def __init__(self, data, convert=[]):
        self.id = int(data[0])
        self.user = int(data[1])
        self.type = str(data[2])
        self.message = str(data[3])
        self.date = date(data[4])

        if 'user' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Users WHERE id={self.user}""")
            self.User = User(c.fetchone())


class Wallet:
    def __init__(self, data, convert=[]):
        self.id = int(data[0])
        self.balance = float(data[1])
        self.owner = int(data[2])

        if 'user' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Users WHERE id={self.owner}""")
            self.Owner = User(c.fetchone())


class OrderInfo:
    def __init__(self, data, convert=[]):
        self.id = int(data[0])
        self.user = int(data[1])
        self.address = str(data[2])
        self.city = int(data[3])
        self.country = int(data[4])
        self.phone = str(data[5])
        self.email = str(data[6])

        if 'user' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Users WHERE id={self.user}""")
            self.User = User(c.fetchone())

        if 'city' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Cities WHERE id={self.city}""")
            self.City = City(c.fetchone())

        if 'country' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Countries WHERE id={self.country}""")
            self.Country = Country(c.fetchone())


class Order:
    def __init__(self, data, convert=[]):
        self.id = int(data[0])
        self.orderedTo = int(data[1])
        self.orderedBy = int(data[2])
        self.orderedProduct = str(data[3])
        self.orderText = str(data[4])
        self.info = int(data[6])
        self.paid = bool(data[7])
        self.date = date(data[8])
        
        if 'user' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Users WHERE id={self.orderedTo}""")
            self.OrderedTo = User(c.fetchone())
            c.execute(f"""SELECT * FROM Users WHERE id={self.orderedBy}""")
            self.OrderedBy = User(c.fetchone())
        
        if 'info' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM OrderInfos WHERE id={self.info}""")
            self.Info = OrderInfo(c.fetchone())


class OrderRating:
    def __init__(self, data, convert=[]):
        self.id = int(data[0])
        self.value = int(data[1])
        self.byUser = int(data[2])
        self.toUser = int(data[3])
        self.forOrder = int(data[4])
        self.date = date(data[5])
        
        if 'user' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Users WHERE id={self.byUser}""")
            self.ByUser = User(c.fetchone())
            c.execute(f"""SELECT * FROM Users WHERE id={self.toUser}""")
            self.ToUser = User(c.fetchone())
        
        if 'order' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Orders WHERE id={self.forOrder}""")
            self.ForOrder = Order(c.fetchone())
