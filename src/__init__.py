from flask import Flask, render_template
from .views import views
from .dashboard import dashboard


def create_app():
    app = Flask(__name__, static_folder='../public', static_url_path='/')
    app.register_blueprint(views)
    app.register_blueprint(dashboard, url_prefix="/dashboard")
    return app
