from flask import Blueprint, render_template, request, make_response
import json
import sqlite3
from .security import authorize, encodeToken, hashPassword, checkPassword


account = Blueprint('account', __name__, template_folder='./templates')


@account.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        data = json.loads(request.data)
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute(f"""SELECT Users.password,Permissions.name 
        FROM 
        Users INNER JOIN Permissions on Users.permission = Permissions.id 
        WHERE username='{data["username"]}'
        """)
        user = c.fetchone()
        if checkPassword(data["password"], user[0]):
            resp = make_response({"success": True})
            authToken = encodeToken({
                "username": data["username"],
                "permission": user[1]
            })
            resp.set_cookie('auth_token', authToken)
            c.execute(f"""INSERT INTO AuthTokens(user,token)
            VALUES
            (
                (SELECT id from Users WHERE username='{data["username"]}'),
                '{authToken}'
            )
            """)
            conn.commit()
        else:
            resp = make_response({"success": False, "error": {
                "type": "WRONG_CREDENTIALS"
            }})
        return resp


@account.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('SELECT name FROM Countries')
        return render_template('signup.html', countries=[country[0] for country in c.fetchall()])
    if request.method == 'POST':
        try:
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            data = json.loads(request.data)
            hashedPassword = hashPassword(data["password"])
            c.execute(f"""INSERT INTO Users(username,password,email,permission,country,city)
            VALUES
            (
                '{data["username"]}',
                '{hashedPassword}',
                '{data["email"]}',
                (SELECT id FROM Permissions WHERE name='{data["permission"]}'),
                (SELECT id FROM Countries WHERE name='{data["country"]}'),
                (SELECT id FROM Cities WHERE name='{data["city"]}')
            )
            """)
            resp = make_response({"success": True})
            authToken = encodeToken({
                "username": data["username"],
                "permission": data["permission"]
            })
            c.execute(f"""INSERT INTO AuthTokens(user,token)
            VALUES
            (
                (SELECT id from Users WHERE username='{data["username"]}'),
                '{authToken}'
            )
            """)
            conn.commit()
            resp.set_cookie('auth_token', authToken)
            return resp
        except sqlite3.Error as e:
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
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""SELECT name FROM Cities 
            WHERE country=(
                SELECT id from Countries WHERE name='{country}'
            );
            """)
            return {"data": [city[0] for city in c.fetchall()], "success": True}
    except Exception as e:
        print(e)
        return {"success": False}


@account.route('/logout')
def logout():
    resp = make_response("Logged out<script>window.open('/','_self')</script>")
    resp.set_cookie('auth_token', '', max_age=0)
    return resp
