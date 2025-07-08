from flask import Flask
import os
from config import Config


def register_blueprints(app: Flask):
    from ior import blueprints

    app.register_blueprint(blueprints.core)


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False)

    app.secret_key = os.urandom(
        30) if not config_class.DEBUG_MODE else "debug_secret"
    app.config.from_object(config_class)

    with app.app_context():
        register_blueprints(app)

        return app
