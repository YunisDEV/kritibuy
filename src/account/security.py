import jwt
import os
import config
import bcrypt
import datetime
from functools import wraps
from flask import abort, request, render_template
from ..db import session, User, AuthToken
import string
import random


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
                q = session.query(AuthToken).filter(AuthToken.user == session.query(
                    User).filter(User.username == token_body["username"]).one().id)
                tokens = [i.token for i in q.all()]
                if token in tokens and token_body["permission"] in allowed:
                    isauth = True
                    q = session.query(User).filter(
                        User.username == token_body["username"])
                    user_data = q.one()
            if not isauth:
                abort(401)
            return f(user_data, *args, **kwargs)
        return wrapper
    return dec


def isauth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('auth_token', False)
        isauth = False
        permissionName = None
        if token:
            token_body = decodeToken(token)
            q = session.query(AuthToken).filter(AuthToken.user == session.query(
                User).filter(User.username == token_body["username"]).one().id)
            tokens = [i.token for i in q.all()]
            if token in tokens:
                isauth = True
                q = session.query(User).filter(
                    User.username == token_body["username"])
                user_data = q.one()
        if not isauth:
            user_data = None
        return f(user_data, *args, **kwargs)
    return wrapper


def generateConKey(length=30):
    characterSet = list(
        set(list(string.ascii_lowercase+string.ascii_uppercase+'0123456789'+'_')))
    setlen = len(characterSet)
    generatedKey = ''
    for i in range(length):
        generatedKey += str(characterSet[random.randrange(0, setlen-1, 1)])
    return generatedKey


def confirmed(f):
    @wraps(f)
    def wrapper(user, *args, **kwargs):
        if user.confirmed:
            print('hello')
            return f(user, *args, **kwargs)
        else:
            return render_template('confirmation_required.html', username=user.username, confirmation_key=user.confirmationKey)
    return wrapper
