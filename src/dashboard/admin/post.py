import sqlite3
from ...schema import *
from flask import make_response

def permissions_post(request):
    resp = make_response()
    return resp