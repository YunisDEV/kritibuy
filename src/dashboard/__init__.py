from flask import Blueprint, render_template, make_response, request
from ..account.security import authorize
import sqlite3
from ..schema import Message

dashboard = Blueprint('dashboard', __name__, template_folder='./templates')


@dashboard.route('/')
@authorize('Admin', 'Personal', 'Business')
def dashboard_main(user):
    if user.Permission.name == 'Personal':
        return f"""<script>window.open('/dashboard/personal','_self')</script>"""
    if user.Permission.name == 'Business':
        return f"""<script>window.open('/dashboard/business','_self')</script>"""
    if user.Permission.name == 'Admin':
        return f"""<script>window.open('/dashboard/admin','_self')</script>"""


#! Personal
@dashboard.route('/personal')
@dashboard.route('/personal/order')
@authorize('Personal')
def personal_main_order(user):
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


@dashboard.route('/personal/stats')
@authorize('Personal')
def personal_stats(user):
    return render_template('personal/stats.html')


@dashboard.route('/personal/wallet')
@authorize('Personal')
def personal_wallet(user):
    return render_template('personal/wallet.html')


#! Business
@dashboard.route('/business')
@authorize('Business')
def business_main(user):
    return f"""{user.id} {user.username}"""


#! Admin
@dashboard.route('/admin')
@authorize('Admin')
def admin_main(user):
    return f"""{user.id} {user.username}"""