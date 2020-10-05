from flask import Blueprint
import config

webhook = Blueprint('webhook',__name__)

@webhook.route('/')
def webhook_main():
    return {'message':'webhook'}