from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/initialize')
def initialize():
    return "Hsello, World!"