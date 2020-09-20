from flask import Flask, render_template
from src.pages import pages
from src.dashboard import dashboard

app = Flask(__name__, static_folder='../public', static_url_path='/')

app.register_blueprint(pages)
app.register_blueprint(dashboard, url_prefix="/dashboard")
