from sqlalchemy import text
from ...db import *
from flask import make_response


def permissions_post(request):
    resp = make_response()
    return resp


def countries_post(request):
    try:
        req = request.get_json()
        session.add(Country(
            name=req["name"],
            alpha2=req["alpha2"],
            alpha3=req["alpha3"],
            flagPath=req["flagPath"]
        ))
        session.commit()
        resp = make_response({"success": True})
        return resp
    except Exception as e:
        resp = make_response({"success":False,"error":str(e)})
        return resp

def cities_post(request):
    try:
        req = request.get_json()
        session.add(City(
            name=req["name"],
            country=session.query(Country).filter(Country.name==req['country']).one().id
        ))
        session.commit()
        resp = make_response({"success": True})
        return resp
    except Exception as e:
        print(e)
        resp = make_response({"success":False,"error":str(e)},500)
        return resp