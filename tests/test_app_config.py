from config import AppConfig


class TestAppConfig(AppConfig):
    TESTING = True
    DEBUG = False

    DATABASE_URI = "sqlite:///:memory:"

    WHIMDB_SERVER_ADDRESS = "127.0.0.1"
    WHIMDB_SERVER_PORT = 6000
