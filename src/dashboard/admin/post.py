from sqlalchemy import text
from ...db import *
from flask import make_response

def permissions_post(request):
    resp = make_response()
    return resp