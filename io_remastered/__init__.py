from flask import Flask
import os
from config.app_config import AppConfig
from io_remastered.db import Database


db = Database()


def register_blueprints(app: Flask):
    from io_remastered import blueprints

    app.register_blueprint(blueprints.core)


def create_app(config_class: AppConfig):
    app = Flask(__name__, instance_relative_config=False)

    app.secret_key = os.urandom(
        30) if not config_class.DEBUG_MODE else "debug_secret"
    app.config.from_object(config_class)

    db.setup(app.config["DATABASE_URI"])
    db.create_all()

    with app.app_context():
        register_blueprints(app)

        return app
