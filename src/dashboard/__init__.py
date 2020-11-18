from flask import Blueprint, render_template, make_response, request, abort, url_for
from ..account.security import authorize, confirmed
import sqlite3
from .admin_panel import panelTree, admin_data_get, admin_data_post, admin_data_delete, admin_data_update
from ..db import session, Message, Permission
from .business_panel import dashboardTree, business_data_get

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
@dashboard.route('/personal/')
@dashboard.route('/personal/order/')
@authorize('Personal')
@confirmed
def personal_main_order(user):
    messages = session.query(Message).filter(Message.user == user.id).all()
    return render_template('personal/index.html', messages=messages)


@dashboard.route('/personal/stats/')
@authorize('Personal')
@confirmed
def personal_stats(user):
    return render_template('personal/stats.html')


@dashboard.route('/personal/wallet/')
@authorize('Personal')
@confirmed
def personal_wallet(user):
    return render_template('personal/wallet.html')


#! Business
@dashboard.route('/business/')
@authorize('Business')
@confirmed
def business_main(user):
    return render_template('business/index.html', pageTitle='Index', tree=dashboardTree, user=user)


@dashboard.route('/business/<folder>/')
@authorize('Business')
@confirmed
def business_folder(user, folder):
    return render_template(f'business/page_index.html', pageTitle=folder, tree=dashboardTree, user=user)


@dashboard.route('/business/inbox/<page>/')
@authorize('Business')
@confirmed
def business_inbox_page(user, page):
    return render_template(f'business/inbox/{page}.html', pageTitle=page, pageParent='inbox', tree=dashboardTree, user=user, data=business_data_get['inbox:'+page](user))


#! Admin
@dashboard.route('/admin/')
@authorize('Admin')
def admin_main(user):
    return render_template('admin/index.html', pageTitle="Index", tree=panelTree)


@dashboard.route('/admin/<folder>/')
@authorize('Admin')
def admin_folder(user, folder):
    return render_template(f'admin/page_index.html', pageTitle=folder, tree=panelTree)


@dashboard.route('/admin/settings/account-settings/', methods=['GET', 'POST'])
@authorize('Admin')
def admin_settings(user):
    if request.method == 'GET':
        return render_template('admin/settings/account_settings.html', pageParent='settings', pageTitle='Account Settings', tree=panelTree, user=user)
    else:
        return render_template('admin/settings/account_settings.html', pageParent='settings', pageTitle='Account Settings', tree=panelTree, user=user)


@dashboard.route('/admin/database/<table>/', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@authorize('Admin')
def admin_database_page(user, table, id=None):
    db_name = None
    for i in panelTree["database"]["indexes"]:
        if i["name"].lower() == table.lower():
            db_name = i["name"]
    if request.method == 'GET':
        data = admin_data_get[db_name](request.args.get('sql', ""))
        updateID = request.args.get('update', '')
        if not updateID == '':
            updateData = None
            for i in data["body"]:
                if i.id == int(updateID):
                    updateData = i
            return render_template(f'admin/database/update/{db_name.lower()}.html', updateID=updateID, updateData=updateData, pageTitle=db_name, pageParent='database', tree=panelTree)
        return render_template(f'admin/database/{db_name.lower()}.html', pageTitle=db_name, pageParent='database', tree=panelTree, data=data)
    elif request.method == 'POST':
        resp = admin_data_post[db_name](request)
        return resp
    elif request.method == 'DELETE':
        resp = admin_data_delete[db_name](request)
        return resp
    elif request.method == 'PATCH':
        resp = admin_data_update[db_name](request)
        return resp


@dashboard.route('/admin/<folder>/<page>/')
@authorize('Admin')
def admin_page(user, folder, page):
    try:
        return render_template(f'admin/{folder}/{page}.html', pageTitle=page, pageParent=folder, tree=panelTree)
    except Exception as e:
        print(e)
        abort(404)
