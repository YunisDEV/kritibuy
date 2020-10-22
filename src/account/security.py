import jwt
import os
import config
import bcrypt
import datetime
from functools import wraps
from flask import abort, request
from ..db import session, User, AuthToken


def encodeToken(payload):
    payload["createdAt"] = datetime.datetime.now().strftime(
        '%Y-%m-%d-%H:%M:%S')
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


def authorize(*allowed):
    def dec(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.cookies.get('auth_token', False)
            isauth = False
            permissionName = None
            if token:
                token_body = decodeToken(token)
                q = session.query(AuthToken).filter(AuthToken.user==session.query(User).filter(User.username==token_body["username"]).one().id)
                tokens = [i.token for i in q.all()]
                if token in tokens and token_body["permission"] in allowed:
                    isauth = True
                    q = session.query(User).filter(User.username==token_body["username"])
                    user_data = q.one()
            if not isauth:
                abort(401)
            return f(user_data, *args, **kwargs)
        return wrapper
    return dec
