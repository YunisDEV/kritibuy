from flask import Flask, render_template
from src.pages import pages
from src.dashboard import dashboard

app = Flask(__name__, static_folder='../public', static_url_path='/')

app.register_blueprint(pages)
app.register_blueprint(dashboard, url_prefix="/dashboard")


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
