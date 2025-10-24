from io_remastered.blueprints.storage.routes import storage

from io_remastered.blueprints.storage.blueprints.files import files_blueprint

storage.register_blueprint(files_blueprint)
