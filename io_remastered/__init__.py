from flask import Flask
import secrets
from config.app_config import AppConfig
from io_remastered.db import Database
from io_remastered.logging import Logging
from io_remastered.io_csrf import CSRF
from io_remastered import app_context_processor_funcs
from io_remastered.extra_modules import RedisCacheDatabase
from io_remastered.authentication import AuthenticationManager


__version__ = "0.0.1"


db = Database()

authentication_cache_db = RedisCacheDatabase(db_id=0)
authentication_manager = AuthenticationManager(auth_db=authentication_cache_db)


def register_blueprints(app: Flask):
    from io_remastered import blueprints

    app.register_blueprint(blueprints.errors)
    app.register_blueprint(blueprints.core)
    app.register_blueprint(blueprints.auth)


def setup_app_modules(app: Flask):
    app_logging = Logging(
        app=app,
        logs_filename="app.log",
        logs_path=app.config.get("LOGS_DIR_PATH"),
        backup_log_files_count=3)

    app_logging.setup()

    db.setup(app.config["DATABASE_URI"])
    db.create_all()

    CSRF(app)

    app.logger.info("app modules setup completed...")


def setup_cache_databases(app: Flask):
    flush_database = True if not app.debug else False

    redis_server_address = app.config.get("REDIS_SERVER_ADDRESS", "")
    redis_server_port = int(app.config.get("REDIS_SERVER_PORT", 0))

    if redis_server_port and redis_server_address:
        authentication_cache_db.setup(
            address=redis_server_address, port=redis_server_port, flush=flush_database)
        
        app.logger.info("authentication_cache_db setup completed...")


def setup_constext_processor(app: Flask):
    app.context_processor(
        lambda: {"get_static_resource": app_context_processor_funcs.get_static_resource})


def create_app(config_class: type[AppConfig]):
    app = Flask(__name__, instance_relative_config=False)

    app.secret_key = secrets.token_hex(
        nbytes=32) if not config_class.DEBUG_MODE else "debug_secret"
    app.config.from_object(config_class)

    setup_app_modules(app)
    setup_cache_databases(app)

    with app.app_context():
        setup_constext_processor(app)
        register_blueprints(app)

        return app
