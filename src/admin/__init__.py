from flask import Flask,Blueprint
from .contentEdit import contentEdit

admin = Blueprint('admin',__name__)
@admin.route('/')
def adminIndex():
    return "Hello"