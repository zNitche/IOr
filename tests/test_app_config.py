from config import AppConfig


class TestAppConfig(AppConfig):
    TESTING = True
    DEBUG = False

    DATABASE_URI = "sqlite:///:memory:"

    REDIS_SERVER_ADDRESS = "127.0.0.1"
    REDIS_SERVER_PORT = "6000"
