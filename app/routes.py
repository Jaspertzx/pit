from app import app
from .util import is_connected

@app.route('/')

@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/initialize')
def initialize():
    if is_connected():
        return "Connected to the internet"
    else:
        return "No internet connection"