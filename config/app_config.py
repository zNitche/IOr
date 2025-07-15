import os
from config import PROJECT_ROOT


class AppConfig:
    DEBUG_MODE = bool(int(os.getenv("DEBUG", 0)))

    APP_HOST = "0.0.0.0"
    APP_PORT = 8080

    SESSION_COOKIE_SAMESITE = "Lax"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DATABASE_ROOT_PATH = os.path.join(PROJECT_ROOT, "database")
    MIGRATIONS_DIR_PATH = os.path.join(DATABASE_ROOT_PATH, "migrations")

    DATABASE_URI = f"sqlite:////{DATABASE_ROOT_PATH}/app.db"
    LOGS_DIR_PATH = os.path.join(PROJECT_ROOT, "logs")

    REDIS_SERVER_ADDRESS = os.getenv("REDIS_SERVER_ADDRESS")
    REDIS_SERVER_PORT = os.getenv("REDIS_SERVER_PORT")
