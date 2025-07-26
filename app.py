from config import AppConfig
from io_remastered import create_app


app = create_app(config_class=AppConfig)


if __name__ == "__main__":
    DEBUG_MODE = app.config["DEBUG"]

    app.run(debug=DEBUG_MODE, host="0.0.0.0", port=8080,
            threaded=True, load_dotenv=False)
