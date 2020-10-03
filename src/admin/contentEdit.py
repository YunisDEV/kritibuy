from flask import Flask, Blueprint

contentEdit = Blueprint('contentEdit',__name__)

@contentEdit.route('/')
def index():
    return 'Hello'