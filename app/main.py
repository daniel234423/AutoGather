from flask import Flask
from .configs import Config
def crear_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    return app

