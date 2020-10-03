from flask import Flask, render_template
from .views import views
from .dashboard import dashboard
from .admin import admin
from .account import account


def create_app():
    app = Flask(__name__, static_folder='../public', static_url_path='/')
    app.register_blueprint(views)
    app.register_blueprint(dashboard, url_prefix="/dashboard")
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(account)
    return app
