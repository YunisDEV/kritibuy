from ..email import send_mail
from flask import Blueprint, render_template, request, make_response, abort
import json
from .security import authorize, encodeToken, hashPassword, checkPassword, generateToken
from ..db import session, Country, City, User, Permission, AuthToken, PasswordRecover, Wallet
import os
import config
from werkzeug.utils import secure_filename
from .utils import make_square
from ..utils import generateBrandNameSuggestion
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
            if not data["password"] == data["passwordConfirm"]:
                raise Exception('Passwords did not match')
            created_user = User(
                username=data["username"],
                password=data["password"],
                email=data["email"],
                permission=session.query(Permission).filter(
                    Permission.name == data["permission"]).one().id,
                country=session.query(Country).filter(
                    Country.name == data["country"]).one().id,
                city=session.query(City).filter(
                    City.name == data["city"]).one().id,
                confirmationKey=generateToken()
            )
            session.add(created_user)
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
            if data['permission'] == 'Business':
                session.add(Wallet(
                    owner=created_user.id
                ))
                session.commit()
                print('Wallet create for '+created_user.username)
            confirmation_link = f'{request.url_root}confirmation/{created_user.username}/{created_user.confirmationKey}'
            print(confirmation_link)
            if not created_user.confirmed:
                send_mail(
                    Subject='Kritibuy - Account Confirmation',
                    To=created_user.email,
                    Content=f'Click link to confirm account. {confirmation_link}',
                    HTML=f"""
                    Click <a href="{confirmation_link}">here</a> to confirm account
                    """
                )
            resp = make_response({"success": True})
            resp.set_cookie('auth_token', authToken)
            return resp
        except Exception as e:
            err = ''
            if str(e).split('\n')[2].endswith('already exists.'):
                err = str(e).split('\n')[2].split(' ')[3].split(
                    ')=(')[0][1:].capitalize() + ' must be unique'
            else:
                err = str(e)
            session.rollback()
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
            defaults = {}
            if permission.name == 'Business':
                defaults["brandName"] = generateBrandNameSuggestion(
                    user.username)
            return render_template(f'confirmation_{permission.name.lower()}.html', user=user, defaults=defaults)
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
                    user.username)+'_logo.'+'png')
                # secure_filename(logo.filename).split('.')[-1]
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
            send_mail(
                Subject="Kritibuy - Account Password Reset",
                To=user.email,
                Content=f'Click link to reset password. {pass_reset_link}',
                HTML=f"""
                    Click <a href="{pass_reset_link}">here</a> to reset account password
                """
            )
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
    passRecover = session.query(PasswordRecover).filter(
        PasswordRecover.active == True and
        PasswordRecover.user == session.query(User).filter(User.username == user
                                                           ).one().id).one()
    token = request.args.get('token')
    if passRecover.token == token:
        if request.method == 'POST':
            data = request.form
            if data["password"] == data["confirm"]:
                try:
                    u = session.query(User).filter(User.username == user).one()
                    u.password = data["password"]
                    passRecover.active = False
                    session.commit()
                    return make_response({"success": True})
                except Exception as e:
                    print(e)
                    return make_response({"success": False, "error": str(e)})
            else:
                return make_response({"success": False, "error": "Passwords do not match"})
                pass
        return render_template('password_reset.html')
    else:
        abort(401)
