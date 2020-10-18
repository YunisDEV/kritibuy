from flask import Flask, render_template
from .views import views
from .dashboard import dashboard
from .account import account
from .chatbot import chatbot


def create_app():
    app = Flask(__name__, static_folder='../public', static_url_path='/')
    app.register_blueprint(views)
    app.register_blueprint(dashboard,url_prefix='/dashboard')
    app.register_blueprint(account)
    app.register_blueprint(chatbot)
    return app
