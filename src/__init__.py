from flask import Flask, render_template
from .views import views
from .dashboard import dashboard
from .account import account
from .webhook import webhook

def create_app():
    app = Flask(__name__, static_folder='../public', static_url_path='/')
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.register_blueprint(views)
    app.register_blueprint(dashboard, url_prefix="/dashboard")
    app.register_blueprint(account)
    app.register_blueprint(webhook,url_prefix='/webhook')
    return app
