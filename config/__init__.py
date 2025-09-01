import os


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
APP_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, 'io_remastered'))


from config.app_config import AppConfig
