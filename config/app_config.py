import os
from config import PROJECT_ROOT


class AppConfig:
    DEBUG_MODE = os.getenv("DEBUG", 0)

    APP_HOST = "0.0.0.0"
    APP_PORT = 8080

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DATABASE_URI = f"sqlite:////{PROJECT_ROOT}/database/app.db"
