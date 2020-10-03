from flask import Blueprint, render_template, redirect

dashboard = Blueprint('dashboard', __name__, template_folder='./templates')


@dashboard.route('/')
def dashboard_main():
    return render_template('inbox.html')


@dashboard.route('/inbox')
def dashboard_inbox():
    return render_template('inbox.html')


@dashboard.route('/stats')
def dashboard_stats():
    return render_template('stats.html')


@dashboard.route('/payments')
def dashboard_payments():
    return render_template('payments.html')
