from flask import Blueprint, render_template, request
import json
import sqlite3

account = Blueprint('account', __name__, template_folder='./templates')


@account.route('/login')
def login():
    return render_template('login.html')


@account.route('/signup')
def signup():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT name FROM Countries')
    return render_template('signup.html', countries=[country[0] for country in c.fetchall()])


@account.route('/get-cities', methods=['POST'])
def getCities():
    try:
        if request.method == 'POST':
            country = json.loads(request.data)["country"]
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(
                f"""SELECT name FROM Cities WHERE country=(SELECT id from Countries WHERE name='{country}')""")
            return {"data": [city[0] for city in c.fetchall()], "success": True}
    except Exception as e:
        print(e)
        return {"success": False}
