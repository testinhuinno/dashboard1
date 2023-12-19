from flask import Flask
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.debug = True

from app import routes
from app.routes import *
