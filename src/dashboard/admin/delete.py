from sqlalchemy import text
from ...db import *
from flask import make_response


def countries_delete(request):
    try:
        id = request.get_json().get('id', '')
        if id == '':
            raise Exception('No ID')
        session.query(Country).filter(Country.id == int(id)).delete()
        session.commit()
        resp = make_response({"success": True}, 200)
        return resp
    except Exception as e:
        print(e)
        resp = make_response({"success": False, "error": str(e)}, 200)
        return resp

def users_delete(request):
    try:
        id = request.get_json().get('id', '')
        if id == '':
            raise Exception('No ID')
        session.query(AuthToken).filter(AuthToken.user == int(id)).delete()
        session.query(User).filter(User.id == int(id)).delete()
        session.commit()
        resp = make_response({"success": True}, 200)
        return resp
    except Exception as e:
        print(e)
        resp = make_response({"success": False, "error": str(e)}, 200)
        return resp

