from sqlalchemy import text
from ...db import *
from flask import make_response
import config
import os
from werkzeug.utils import secure_filename

def permissions_post(request):
    resp = make_response()
    return resp


def countries_post(request):
    try:
        req = request.form
        flag = request.files["flagPath"]
        flag_directory = os.path.join(config.UPLOAD_DIR_COUNTRY_FLAGS,str(req["alpha3"].lower())+'_flag.'+secure_filename(flag.filename).split('.')[-1])
        flag.save(flag_directory)
        flag_dir = flag_directory.split('public')[1]
        session.add(Country(
            name=req["name"],
            alpha2=req["alpha2"],
            alpha3=req["alpha3"],
            flagPath=flag_dir
        ))
        session.commit()
        resp = make_response({"success":True})
        return resp
    except Exception as e:
        print('Error: ',str(e))
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