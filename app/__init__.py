from flask import Flask
from .util import is_connected

app = Flask(__name__)

from app import routes