from flask import current_app
from io_remastered import db

from io_remastered.blueprints.core.routes import core


@current_app.teardown_appcontext
def teardown_appcontext(exception=None):
    db.close_session(exception=exception)
