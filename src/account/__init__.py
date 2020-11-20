from flask import Blueprint, render_template, request, make_response, abort
import json
from .security import authorize, encodeToken, hashPassword, checkPassword, generateToken
from ..db import session, Country, City, User, Permission, AuthToken, PasswordRecover
import os
import config
from werkzeug.utils import secure_filename
from .utils import make_square
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
                confirmationKey=generateToken()
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
        if permission.name == 'Personal':
            try:
                user.fullName = data['fullName']
                user.address = data['address']
                user.phone = data['phone']
                user.confirmed = True
                session.commit()
                return make_response({"success": True})
            except Exception as e:
                print(e)
                return make_response({"success": False, "error": str(e)})
        else:
            try:
                data = request.form
                logo = request.files["brandLogo"]
                logo_directory = os.path.join(config.UPLOAD_DIR_BRAND_LOGOS, str(
                    user.username)+'_logo.'+secure_filename(logo.filename).split('.')[-1])

                logo.save(logo_directory)
                logo_dir = logo_directory.split('public')[1]

                editedLogo = make_square(logo_directory)
                editedLogo.save(logo_directory)

                user.fullName = data["fullName"]
                user.address = data["address"]
                user.phone = data["phone"]
                user.brandName = data["brandName"]
                user.brandProductTypes = data["brandProductTypes"].split(',')
                user.brandNameSynonyms = data["brandNameSynonyms"].split(',')
                user.brandLogoPath = logo_dir
                user.confirmed = True
                session.commit()
                return make_response("""<script>window.open('/dashboard/business','_self')</script>""")
            except Exception as e:
                print(e)
                return make_response({"success": False, "error": str(e)})


@account.route('/password-recover', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        data = request.form
        user = session.query(User).filter(User.username ==
                                          data["username"] and User.email == data["email"]).one()
        if user:
            oldtokens = session.query(PasswordRecover).filter(
                PasswordRecover.user == user.id).all()
            for oT in oldtokens:
                oT.active = False
            generatedToken = generateToken()
            session.add(PasswordRecover(
                user=user.id,
                token=generatedToken
            ))
            pass_reset_link = f'{request.url_root}pass-reset/{user.username}?token={generatedToken}'
            print(pass_reset_link)
            session.commit()
            return make_response({"success": True})
        else:
            return make_response({"success": False})
        return
    if request.method == 'GET':
        if request.args.get('success') == 'true':
            return render_template('success_message.html', message='Check your email for password recover link')
        pass
        return render_template('password_recover.html')


@account.route('/pass-reset/<user>', methods=['GET', 'POST'])
def pass_reset(user):
    passRecover = session.query(PasswordRecover).filter(PasswordRecover.active == True and
                                                        PasswordRecover.user == session.query(User).filter(User.username == user).one().id).one()
    token = request.args.get('token')
    if passRecover.token == token:
        if request.method == 'POST':
            data = request.form
            if data["password"] == data["confirm"]:
                hp = hashPassword(data["password"])
                u = session.query(User).filter(User.username == user).one()
                u.password = hp
                passRecover.active = False
                session.commit()
                return make_response({"success": True})
                pass
            else:
                return make_response({"success": False, "error": "Passwords do not match"})
                pass
        return render_template('password_reset.html')
    else:
        abort(401)
