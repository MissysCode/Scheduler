from flask import Flask
from .config import Config
from .database import init_db, close_db
from .routes import register_routes


def create_app():
    prefix = Config.URL_PREFIX

    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="templates",
        static_folder="static",
        static_url_path=f"{prefix}/static" if prefix else "/static"
    )
    app.config.from_object(Config)

    init_db(app)
    register_routes(app)

    app.teardown_appcontext(close_db)

    return app