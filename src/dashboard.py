from flask import Blueprint, render_template, redirect

dashboard = Blueprint('dashboard', __name__, template_folder='../views')


@dashboard.route('/')
def dashboard_main():
    return render_template('redirect.html', link="/dashboard/inbox")


@dashboard.route('/inbox')
def dashboard_inbox():
    return render_template('dashboard/inbox.html')


@dashboard.route('/stats')
def dashboard_stats():
    return render_template('dashboard/stats.html')


@dashboard.route('/payments')
def dashboard_payments():
    return render_template('dashboard/payments.html')


@dashboard.route('/contact')
def dashboard_contact():
    return render_template('dashboard/contact.html')
