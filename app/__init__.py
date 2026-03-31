from flask import Flask
from .config import Config
from .database import init_db
from .routes import register_routes


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    init_db(app)
    register_routes(app)

    return app