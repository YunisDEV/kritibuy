from flask import Blueprint, render_template, request, make_response, abort
import json
from .security import authorize, encodeToken, hashPassword, checkPassword, generateConKey
from ..db import session, Country, City, User, Permission, AuthToken
import os
import config
from werkzeug.utils import secure_filename

account = Blueprint('account', __name__, template_folder='./templates')


@account.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        data = json.loads(request.data)
        user = session.query(User.password, Permission.name).join(
            Permission).filter(User.username == data["username"]).one()
        if checkPassword(data["password"], user.password):
            authToken = encodeToken({
                "username": data["username"],
                "permission": user.name
            })
            resp = make_response({"success": True})
            resp.set_cookie('auth_token', authToken)
            session.add(AuthToken(
                user=session.query(User).filter(
                    User.username == data["username"]).one().id,
                token=authToken
            ))
            session.commit()
        else:
            resp = make_response({"success": False, "error": {
                "type": "WRONG_CREDENTIALS"
            }})
        return resp


@account.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        countries = list(map(lambda x: x.name, session.query(
            Country.name).order_by(Country.name)))
        return render_template('signup.html', countries=countries)
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            hashedPassword = hashPassword(data["password"])
            session.add(User(
                username=data["username"],
                password=hashedPassword,
                email=data["email"],
                permission=session.query(Permission).filter(
                    Permission.name == data["permission"]).one().id,
                country=session.query(Country).filter(
                    Country.name == data["country"]).one().id,
                city=session.query(City).filter(
                    City.name == data["city"]).one().id,
                confirmationKey=generateConKey()
            ))
            authToken = encodeToken({
                "username": data["username"],
                "permission": data["permission"]
            })
            session.add(AuthToken(
                user=session.query(User).filter(
                    User.username == data["username"]).one().id,
                token=authToken
            ))
            session.commit()
            resp = make_response({"success": True})
            resp.set_cookie('auth_token', authToken)
            return resp
        except Exception as e:
            err = {}
            print(e)
            if str(e).startswith('UNIQUE'):
                err["type"] = 'UNIQUE'
                err["value"] = str(e).split(': ')[1].split('.')[1].capitalize()
            return {"success": False, "error": err}


@account.route('/get-cities', methods=['POST'])
def getCities():
    try:
        if request.method == 'POST':
            country = json.loads(request.data)["country"]
            q = session.query(City.name).filter(
                City.country == session.query(Country).filter(
                    Country.name == country
                ).one().id
            ).order_by(City.name)
            return {"data": [city.name for city in q.all()], "success": True}
    except Exception as e:
        print(e)
        return {"success": False}


@account.route('/get-countries', methods=['GET'])
def getCountries():
    try:
        if request.method == 'GET':
            q = session.query(Country.name).order_by(Country.name)
            return {"data": [country.name for country in q.all()], "success": True}
    except Exception as e:
        print(e)
        return {"success": False}


@account.route('/logout')
def logout():
    resp = make_response("<script>window.open('/','_self')</script>")
    resp.set_cookie('auth_token', '', max_age=0)
    return resp


@account.route('/confirmation/<user>/<con_key>', methods=['GET', 'POST'])
def confirmation(user, con_key):
    user = session.query(User).filter(User.username == user).one()
    permission = session.query(Permission).filter(
        Permission.id == user.permission).one()
    if request.method == 'GET':
        if user.confirmationKey == con_key and permission.name in ['Personal', 'Business']:
            return render_template(f'confirmation_{permission.name.lower()}.html', user=user)
        else:
            abort(401)
    elif request.method == 'POST':
        data = request.get_json()
        if permission.name=='Personal':
            try:
                user.fullName = data['fullName']
                user.address = data['address']
                user.phone = data['phone']
                user.confirmed = True
                session.commit()
                return make_response({"success":True})
            except Exception as e:
                print(e)
                return make_response({"success":False,"error":str(e)})
        else:
            try:
                data = request.form
                logo = request.files["brandLogo"]
                logo_directory = os.path.join(config.UPLOAD_DIR_BRAND_LOGOS,str(user.username)+'_logo.'+secure_filename(logo.filename).split('.')[-1])
                logo.save(logo_directory)
                logo_dir = logo_directory.split('public')[1]
                user.fullName = data["fullName"]
                user.address = data["address"]
                user.phone = data["phone"]
                user.brandName = data["brandName"]
                user.brandLogoPath = logo_dir
                user.confirmed = True
                session.commit()
                return make_response("""<script>window.open('/dashboard/business','_self')</script>""")
            except Exception as e:
                print(e)
                return make_response({"success":False,"error":str(e)})


@account.route('/password-recover', methods=['GET', 'POST'])
def forgot_password():
    return ''


@account.route('/pass-reset', methods=['GET', 'POST'])
def pass_reset():
    return request.args.get('token')
