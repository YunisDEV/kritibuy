from sqlalchemy import text
from ...db import *
from flask import make_response
import config
import os
from werkzeug.utils import secure_filename


def countries_update(request):
    try:
        id = request.args.get('id', '')
        if not id:
            raise Exception('ID is not in arguments')
        country = session.query(Country).filter(Country.id == int(id)).one()
        country.name = request.form["name"]
        country.alpha2 = request.form["alpha2"]
        country.alpha3 = request.form["alpha3"]
        flag = request.files.get('flagPath', None)
        print(flag)
        if flag:
            flag_directory = os.path.join(config.UPLOAD_DIR_COUNTRY_FLAGS, str(
                request.form["alpha3"].lower())+'_flag.'+secure_filename(flag.filename).split('.')[-1])
            flag.save(flag_directory)
            flag_dir = flag_directory.split('public')[1]
            country.flagPath = flag_dir
        session.commit()
        resp = make_response({"success": True}, 200)
        return resp
    except Exception as e:
        print(e)
        resp = make_response({"success": False, "error": str(e)}, 200)
        return resp
