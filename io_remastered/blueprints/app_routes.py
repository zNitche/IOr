from flask import current_app
from io_remastered import db, i18n


@current_app.teardown_appcontext
def teardown_appcontext(exception=None):
    db.close_session(exception=exception)


@current_app.before_request
def before_request():
    i18n.before_request()
