from itertools import product
from flask import Blueprint, render_template, make_response, request, abort, url_for
from sqlalchemy.util.langhelpers import methods_equivalent
from ..account.security import authorize, confirmed, hashPassword, checkPassword, generateToken
from .admin_panel import panelTree, admin_data_get, admin_data_post, admin_data_delete, admin_data_update
from ..db import session, Message, Permission, Country, City, User, PasswordRecover
from .business_panel import dashboardTree, business_data_get
import json

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


@dashboard.route('/business/add-product-to-list', methods=['POST'])
@authorize('Business')
@confirmed
def add_product_to_list(user):
    if request.method == 'POST':
        try:
            product_name = json.loads(request.data)["productName"]
            product_list = user.brandProductTypes
            product_list.append(str(product_name))
            user.brandProductTypes = product_list
            print(user.__dict__)
            session.add(user)
            session.commit()
            return make_response({"success": True})
        except Exception as e:
            print(e)
            return make_response({"success": False,"error":str(e)})


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
def admin_account_settings(user):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.fullName = request.form['fullName'] or None
        user.address = request.form['address'] or None
        user.phone = request.form['phone'] or None
        user.phone = request.form['phone'] or None
        user.country = session.query(Country).filter(
            Country.name == request.form['country']).one().id
        user.city = session.query(City).filter(
            City.name == request.form['city']).one().id
        session.commit()
    user_country = session.query(Country).filter(
        Country.id == user.country).one()
    countries = session.query(Country)
    user_city = session.query(City).filter(City.id == user.city).one()
    return render_template('admin/settings/account_settings.html', pageParent='settings', pageTitle='Account Settings', tree=panelTree, user=user, city=user_city, country=user_country, countries=countries)


@dashboard.route('/admin/settings/password-recover/', methods=['GET', 'POST'])
@authorize('Admin')
def admin_password_recover(user):
    status = None
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        oldtokens = session.query(PasswordRecover).filter(
            PasswordRecover.user == user.id).all()
        for oT in oldtokens:
            oT.active = False
        recover_token = generateToken()
        session.add(PasswordRecover(
            user=user.id,
            token=recover_token
        ))
        session.commit()
        pass_reset_link = f'{request.url_root}pass-reset/{user.username}?token={recover_token}'
        print(pass_reset_link)
        # send link to email
        status = True
    return render_template('admin/settings/password_recover.html', pageParent='settings', pageTitle='Password Recover', tree=panelTree, user=user, status=status or False)


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
