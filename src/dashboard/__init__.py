from flask import Blueprint, render_template, make_response, request
from ..account.security import authorize
import sqlite3
from ..schema import Message

dashboard = Blueprint('dashboard', __name__, template_folder='./templates')


@dashboard.route('/')
@authorize('Admin', 'Personal', 'Business')
def dashboard_main(user):
    if user.Permission.name == 'Personal':
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        print(user.id)
        c.execute(f"""SELECT * FROM Messages WHERE user={user.id}""")
        messages_list = c.fetchall()
        print(messages_list)
        messages = []
        for i in messages_list:
            messages.append(Message(i))
        print(messages)
        return render_template('personal/index.html', messages=messages)
    if user.Permission.name == 'Business':
        print('rendering business UI')
        return render_template('business/index.html')
    return 'blabla'


@dashboard.route('/order')
@authorize('Personal')
def dashboard_order(user):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    print(user.id)
    c.execute(f"""SELECT * FROM Messages WHERE user={user.id}""")
    messages_list = c.fetchall()
    print(messages_list)
    messages = []
    for i in messages_list:
        messages.append(Message(i))
    print(messages)
    return render_template('personal/index.html', messages=messages)


@dashboard.route('/stats')
def dashboard_stats():
    return render_template('personal/stats.html')


@dashboard.route('/wallet')
def dashboard_payments():
    return render_template('personal/wallet.html')
