from sqlalchemy import text
from ...db import *
from flask import make_response

def countries_update(request):
    try:
        id = request.args.get('id', '')
        if not id:
            raise Exception('ID is not in arguments')
        country = session.query(Country).filter(Country.id==int(id)).one()
        country.name = request.form["name"]
        country.alpha2 = request.form["alpha2"]
        country.alpha3 = request.form["alpha3"]
        country.flagPath = request.form["flagPath"]
        session.commit()
        resp = make_response({"success": True}, 200)
        return resp
    except Exception as e:
        print(e)
        resp = make_response({"success": False, "error": str(e)}, 200)
        return resp
