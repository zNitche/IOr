from config import AppConfig
from io_remastered import create_app


app = create_app(config_class=AppConfig)


if __name__ == "__main__":
    APP_PORT = app.config["APP_PORT"]
    APP_HOST = app.config["APP_HOST"]
    DEBUG_MODE = app.config["DEBUG"]

    app.run(debug=DEBUG_MODE, host=APP_HOST, port=APP_PORT,
            threaded=True, load_dotenv=False)
