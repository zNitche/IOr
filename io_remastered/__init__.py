from flask import Flask
import secrets
from config.app_config import AppConfig
from io_remastered.db import Database
from io_remastered.logging import Logging
from io_remastered.csrf_protection import CSRF


__version__ = "0.0.1"


db = Database()


def register_blueprints(app: Flask):
    from io_remastered import blueprints

    app.register_blueprint(blueprints.core)


def setup_app_modules(app: Flask):
    app_logging = Logging(
        app=app,
        logs_filename="app.log",
        logs_path=app.config.get("LOGS_DIR_PATH"),
        backup_log_files_count=3)

    app_logging.setup()

    db.setup(app.config["DATABASE_URI"])
    db.create_all()

    csrf = CSRF(app)
    csrf.setup()


def create_app(config_class: type[AppConfig]):
    app = Flask(__name__, instance_relative_config=False)

    app.secret_key = secrets.token_hex(
        nbytes=32) if not config_class.DEBUG_MODE else "debug_secret"
    app.config.from_object(config_class)

    setup_app_modules(app)

    with app.app_context():
        register_blueprints(app)

        return app
