import sqlite3


class Permission:
    def __init__(self, data):
        self.id = data[0]
        self.name = data[1]


class Country:
    def __init__(self, data):
        self.id = data[0]
        self.name = data[1]
        self.alpha2 = data[2]
        self.alpha3 = data[3]
        self.flagPath = data[4]


class City:
    def __init__(self, data, convert=[]):
        self.id = data[0]
        self.name = data[1]
        self.country = data[2]
        if 'country' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Countries WHERE id={data[2]}""")
            self.Country = Country(c.fetchone())


class User:
    def __init__(self, data, convert=[]):
        self.id = data[0]
        self.username = data[1]
        self.password = data[2]
        self.email = data[3]
        self.permission = data[4]
        self.fullName = data[5]
        self.address = data[6]
        self.phone = data[7]
        self.country = data[8]
        self.city = data[9]
        self.brandLogoPath = data[10]
        self.brandName = data[11]
        self.createdAt = data[12]
        self.brandProductTypes = data[13]
        self.active = bool(data[14])
        if 'permission' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Permissions WHERE id={data[4]}""")
            self.Permission = Permission(c.fetchone())
        if 'country' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(
                f"""SELECT * FROM Countries WHERE id={data[8]}""")
            self.Country = Country(c.fetchone())
        if 'city' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(
                f"""SELECT * FROM Cities WHERE id={data[9]}""")
            self.City = City(c.fetchone())


class AuthToken:
    def __init__(self, data, convert=[]):
        self.id = data[0]
        self.user = data[1]
        self.token = data[2]
        if 'user' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(
                f"""SELECT * FROM Users WHERE id={data[1]}""")
            self.User = User(c.fetchone())


class Payment:
    def __init__(self, data, convert=[]):
        self.id = data[0]
        self.fromUser = data[1]
        self.toUser = data[2]
        self.amount = data[3]
        self.date = data[3]
        if 'user' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Users WHERE id={data[1]}""")
            self.FromUser = User(c.fetchone())
            c.execute(f"""SELECT * FROM Users WHERE id={data[2]}""")
            self.ToUser = User(c.fetchone())


class Report:
    def __init__(self, data, convert=[]):
        self.id = data[0]
        self.reporter = data[1]
        self.header = data[2]
        self.body = data[3]
        self.date = data[4]
        if 'user' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Users WHERE id={data[1]}""")
            self.Reporter = User(c.fetchone())


class Message:
    def __init__(self, data, convert=[]):
        self.id = data[0]
        self.user = data[1]
        self.type = data[2]
        self.message = data[3]
        self.date = data[4]
        if 'user' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Users WHERE id={data[1]}""")
            self.User = User(c.fetchone())


class Wallet:
    def __init__(self, data, convert=[]):
        self.id = data[0]
        self.balance = data[1]
        self.owner = data[2]
        if 'user' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Users WHERE id={data[2]}""")
            self.Owner = User(c.fetchone())

class OrderInfo:
    def __init__(self, data, convert=[]):
        self.id = data[0]

class Order:
    def __init__(self, data, convert=[]):
        self.id = data[0]
        self.orderedTo = data[1]
        self.orderedBy = data[2]
        self.orderText = data[3]
        self.orderPrice = data[4]
        self.info = data[5]
        self.paid = data[6]
        self.date = data[7]
        if 'user' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Users WHERE id={data[1]}""")
            self.OrderedTo = User(c.fetchone())
            c.execute(f"""SELECT * FROM Users WHERE id={data[2]}""")
            self.OrderedBy = User(c.fetchone())
        if 'info' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM OrderInfos WHERE id={data[5]}""")
            self.Info = OrderInfo(c.fetchone())
            

class OrderRating:
    def __init__(self, data, convert=[]):
        self.id = data[0]
        self.value = data[1]
        self.byUser = data[2]
        self.toUser = data[3]
        self.forOrder = data[4]
        self.date = data[5]
        if 'user' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Users WHERE id={data[2]}""")
            self.ByUser = User(c.fetchone())
            c.execute(f"""SELECT * FROM Users WHERE id={data[3]}""")
            self.ToUser = User(c.fetchone())
        if 'order' in convert or convert == "*":
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT * FROM Orders WHERE id={data[4]}""")
            self.ForOrder = Order(c.fetchone())
