from flask import Flask
import secrets
from config.app_config import AppConfig
from io_remastered.db import Database
from io_remastered.io_logging import AppLogging
from io_remastered.io_csrf import CSRF
from io_remastered.io_i18n import I18n
from io_remastered.extra_modules import RedisCacheDatabase
from io_remastered.authentication import AuthenticationManager

__version__ = "0.0.1"


db = Database()

authentication_cache_db = RedisCacheDatabase(db_id=0)
authentication_manager = AuthenticationManager(auth_db=authentication_cache_db)

i18n = I18n(translations_path="./i18n")


def register_blueprints(app: Flask):
    from io_remastered import blueprints

    app.register_blueprint(blueprints.errors)
    app.register_blueprint(blueprints.auth)
    app.register_blueprint(blueprints.core)
    app.register_blueprint(blueprints.upload)
    app.register_blueprint(blueprints.storage)


def setup_app_modules(app: Flask):
    app_logging = AppLogging(
        app=app,
        logs_filename="app.log",
        logs_path=app.config.get("LOGS_DIR_PATH"),
        backup_log_files_count=3)

    app_logging.setup()

    db.setup(app.config["DATABASE_URI"])
    db.create_all()

    authentication_manager.setup(
        default_auth_token_ttl=app.config.get("AUTH_TOKEN_LIFESPAN", None))

    CSRF.setup(app)
    i18n.setup(app)

    app.logger.info("app modules setup completed...")


def setup_cache_databases(app: Flask):
    flush_database = True if not app.debug else False

    redis_server_address = app.config.get("REDIS_SERVER_ADDRESS", "")
    redis_server_port = int(app.config.get("REDIS_SERVER_PORT", 0))

    authentication_cache_db.setup(
        address=redis_server_address, port=redis_server_port, flush=flush_database)

    app.logger.info("authentication_cache_db setup completed...")


def create_app(config_class: type[AppConfig]):
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object(config_class)
    app.secret_key = secrets.token_hex(
        nbytes=32) if not app.debug else "debug_secret"

    setup_app_modules(app)
    setup_cache_databases(app)

    with app.app_context():
        from io_remastered.jinja_context import setup_constext_processor, setup_template_filters

        setup_constext_processor(app)
        setup_template_filters(app)

        register_blueprints(app)

        app.logger.info("app has been created")

        return app
