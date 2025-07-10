from flask import Flask
import os
from config.app_config import AppConfig
from io_remastered.db import Database
from io_remastered.logging import Logging


__version__ = "0.0.1"


db = Database()


def register_blueprints(app: Flask):
    from io_remastered import blueprints

    app.register_blueprint(blueprints.core)


def create_app(config_class: type[AppConfig]):
    app = Flask(__name__, instance_relative_config=False)

    app.secret_key = os.urandom(
        30) if not config_class.DEBUG_MODE else "debug_secret"
    app.config.from_object(config_class)

    db.setup(app.config["DATABASE_URI"])
    db.create_all()

    app_logging = Logging(
        app=app,
        logs_filename="app.log",
        logs_path=app.config.get("LOGS_DIR_PATH"),
        backup_log_files_count=3)

    app_logging.setup()

    with app.app_context():
        register_blueprints(app)

        return app
