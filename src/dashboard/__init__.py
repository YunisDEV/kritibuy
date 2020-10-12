from flask import Blueprint, render_template, make_response, request
from ..account.security import authorize

dashboard = Blueprint('dashboard', __name__, template_folder='./templates')


@dashboard.route('/')
@authorize('Admin', 'Personal', 'Business')
def dashboard_main(user,uPermission):
    if uPermission == 'Personal':
        return render_template('personal/index.html')
    if uPermission == 'Business':
        print('rendering business UI')
        return render_template('business/index.html')
    return 'blabla'


@dashboard.route('/inbox')
def dashboard_inbox():
    return render_template('personal/inbox.html')


@dashboard.route('/stats')
def dashboard_stats():
    return render_template('personal/stats.html')


@dashboard.route('/wallet')
def dashboard_payments():
    return render_template('personal/wallet.html')
