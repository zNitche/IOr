__version__ = "1.1.4"


from flask import Flask
import secrets
from config.app_config import AppConfig
from io_remastered.db import Database
from io_remastered.io_logging import AppLogging
from io_remastered.io_csrf import CSRF
from io_remastered.io_i18n import I18n
from io_remastered.extra_modules import CacheDatabase
from io_remastered.authentication import AuthenticationManager


db = Database()

authentication_cache_db = CacheDatabase(db_id=0)
authentication_manager = AuthenticationManager(auth_db=authentication_cache_db)

i18n = I18n(translations_path="./i18n")


def generate_secret(is_debug=False):
    return secrets.token_hex(
        nbytes=32) if not is_debug else "debug_secret"


def register_blueprints(app: Flask):
    from io_remastered import blueprints

    app.register_blueprint(blueprints.errors_blueprint)
    app.register_blueprint(blueprints.auth_blueprint)
    app.register_blueprint(blueprints.core_blueprint)
    app.register_blueprint(blueprints.upload_blueprint)
    app.register_blueprint(blueprints.storage_blueprint)
    app.register_blueprint(blueprints.share_blueprint)
    app.register_blueprint(blueprints.account_blueprint)


def register_routes(app: Flask):
    from io_remastered import blueprints

    app.add_url_rule(rule="/static/<path:filename>", endpoint="static",
                     view_func=blueprints.app_routes.static_content_handler)


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

    whimdb_server_address = app.config.get("WHIMDB_SERVER_ADDRESS", "")
    whimdb_server_port = int(app.config.get("WHIMDB_SERVER_PORT", 0))

    authentication_cache_db.setup(server_address=whimdb_server_address,
                                  server_port=whimdb_server_port, flush=flush_database)

    app.logger.info("authentication_cache_db setup completed...")


def create_app(config_class: type[AppConfig]):
    app = Flask(__name__, instance_relative_config=False, static_folder=None)

    app.config.from_object(config_class)
    app.secret_key = generate_secret(is_debug=app.debug)

    setup_app_modules(app)
    setup_cache_databases(app)

    with app.app_context():
        from io_remastered.jinja_context import setup_constext_processor, setup_template_filters

        register_routes(app)
        register_blueprints(app)

        setup_constext_processor(app)
        setup_template_filters(app)

        app.logger.info("app has been created")

        return app
