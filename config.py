import os
DEBUG = True
PORT = os.environ.get('FLASK_PORT', 5000)
SECRET_KEY = os.environ.get('KRITIBUY_SECRET','hello')