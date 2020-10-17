import os
DEBUG = True
PORT = os.environ.get('FLASK_PORT', 5000)
SECRET_KEY = os.environ.get('KRITIBUY_SECRET','token')
WEBHOOK_AUTH = os.environ.get('WEBHOOK_AUTH','token')
DIALOG_FLOW_AUTH = os.environ.get('DIALOG_FLOW_AUTH','auth')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'google_services_key.json'