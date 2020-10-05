from flask import Flask, Blueprint

admin = Blueprint('admin', __name__)


@admin.route('/content')
def content():
    return 'aaaa'
