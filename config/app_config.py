import os
from datetime import timedelta
from config import PROJECT_ROOT


class AppConfig:
    DEBUG = bool(int(os.getenv("DEBUG", 0)))

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = bool(int(os.getenv("HTTPS_ONLY", 1)))
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)

    DATABASE_ROOT_PATH = os.path.join(PROJECT_ROOT, "database")
    MIGRATIONS_DIR_PATH = os.path.join(DATABASE_ROOT_PATH, "migrations")

    DATABASE_URI = f"sqlite:////{DATABASE_ROOT_PATH}/app.db"

    LOGS_DIR_PATH = os.path.join(PROJECT_ROOT, "logs")

    WHIMDB_SERVER_ADDRESS = os.getenv("WHIMDB_SERVER_ADDRESS")
    WHIMDB_SERVER_PORT = os.getenv("WHIMDB_SERVER_PORT")

    AUTH_TOKEN_LIFESPAN = int(os.getenv("AUTH_TOKEN_LIFESPAN", 600))

    STORAGE_ROOT_PATH = os.path.join(PROJECT_ROOT, "files_storage")
    STORAGE_TMP_ROOT_PATH = os.path.join(STORAGE_ROOT_PATH, "tmp")

    MAX_CONTENT_LENGTH = int(os.getenv("MAX_REQUEST_SIZE_MB", 15)) * 1_000_000
    FILE_UPLOAD_CHUNK_SIZE_MB = int(os.getenv("FILE_UPLOAD_CHUNK_SIZE_MB", 10)) * 1_000_000
