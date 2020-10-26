from flask import Blueprint, render_template, make_response, request, abort, url_for
from ..account.security import authorize
import sqlite3
from .admin_panel import panelTree, db_data_get, db_data_post, db_data_delete
from ..db import session, Message, Permission

dashboard = Blueprint('dashboard', __name__, template_folder='./templates')


@dashboard.route('/')
@authorize('Admin', 'Personal', 'Business')
def dashboard_main(user):
    permissionName = session.query(Permission).filter(
        Permission.id == user.permission
    ).one().name
    if permissionName == 'Personal':
        return f"""<script>window.open('/dashboard/personal','_self')</script>"""
    if permissionName == 'Business':
        return f"""<script>window.open('/dashboard/business','_self')</script>"""
    if permissionName == 'Admin':
        return f"""<script>window.open('/dashboard/admin','_self')</script>"""


#! Personal
@dashboard.route('/personal')
@dashboard.route('/personal/order')
@authorize('Personal')
def personal_main_order(user):
    messages = session.query(Message).filter(Message.user == user.id).all()
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
@dashboard.route('/admin/')
@authorize('Admin')
def admin_main(user):
    return render_template('admin/index.html', pageTitle="Index", tree=panelTree)


@dashboard.route('/admin/<folder>/')
@authorize('Admin')
def admin_folder(user, folder):
    return render_template(f'admin/page_index.html', pageTitle=folder, tree=panelTree)


@dashboard.route('/admin/database/<table>/', methods=['GET', 'POST', 'DELETE'])
@authorize('Admin')
def admin_database_page(user, table):
    db_name = None
    for i in panelTree["database"]["indexes"]:
        if i["name"].lower() == table.lower():
            db_name = i["name"]
    if request.method == 'GET':
        data = db_data_get[db_name](request.args.get('sql', ""))
        return render_template(f'admin/database/{db_name.lower()}.html', pageTitle=db_name, pageParent='database', tree=panelTree, data=data)
    elif request.method == 'POST':
        resp = db_data_post[db_name](request)
        return resp
    elif request.method == 'DELETE':
        resp = db_data_delete[db_name](request)
        return resp


@dashboard.route('/admin/<folder>/<page>/')
@authorize('Admin')
def admin_page(user, folder, page):
    try:
        return render_template(f'admin/{folder}/{page}.html', pageTitle=page, pageParent=folder, tree=panelTree)
    except Exception as e:
        print(e)
        abort(404)
