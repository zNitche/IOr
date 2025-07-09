import os
from load_dotenv import load_dotenv


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
APP_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, 'io_remastered'))


load_dotenv(os.path.join(PROJECT_ROOT, ".env"))


from config.app_config import AppConfig
