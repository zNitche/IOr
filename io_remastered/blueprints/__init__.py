from flask import current_app
from io_remastered import db

from io_remastered.blueprints.core.routes import core
from io_remastered.blueprints.auth.routes import auth
from io_remastered.blueprints.upload.routes import upload
from io_remastered.blueprints.storage.routes import storage
from io_remastered.blueprints.errors.routes import errors


@current_app.teardown_appcontext
def teardown_appcontext(exception=None):
    db.close_session(exception=exception)
