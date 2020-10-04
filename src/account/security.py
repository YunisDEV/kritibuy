import jwt
import os
import config
import bcrypt
import sqlite3
import datetime

def encodeToken(payload):
    payload["createdAt"] = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    encodedJWT = jwt.encode(payload, config.SECRET_KEY,
                            algorithm='HS256').decode()
    return encodedJWT


def decodeToken(token):
    decodedJWT = jwt.decode(token, config.SECRET_KEY, algorithm='HS256')
    return decodedJWT


def hashPassword(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def checkPassword(password, hashedPassword):
    return bool(bcrypt.checkpw(password.encode(), hashedPassword.encode()))


def isauth(request):
    token = request.cookies.get('auth_token', False)
    if token:
        token_body = decodeToken(token)
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute(
            f"""SELECT token FROM AuthTokens WHERE user=(SELECT id FROM Users WHERE username='{token_body["username"]}')""")
        fetchedToken = c.fetchone()[0]
        if token == fetchedToken:
            return True
    return False
