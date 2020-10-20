from flask import Flask, render_template, abort
from .views import views
from .dashboard import dashboard
from .account import account
from .chatbot import chatbot
from werkzeug.exceptions import HTTPException


def create_app():
    app = Flask(__name__, static_folder='../public',
                static_url_path='/', template_folder='./templates')
    app.register_blueprint(views)
    app.register_blueprint(dashboard, url_prefix='/dashboard')
    app.register_blueprint(account)
    app.register_blueprint(chatbot)

    @app.errorhandler(HTTPException)
    def page_not_found(e):
        return render_template('error_page.html', code=e.code, name=e.name), e.code

    return app
