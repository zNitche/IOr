import os
from flask import current_app, send_file, request, Response
from io_remastered import db, i18n
from config import APP_ROOT


@current_app.teardown_appcontext
def teardown_appcontext(exception=None):
    db.close_session(exception=exception)


@current_app.before_request
def before_request():
    i18n.before_request()


# @current_app.route("/static/<path:filename>")
def static_content_handler(filename: str):
    forbdidden_characters = ["..", "~", "&", "//", "\\"]
    parsed_filename = filename

    for char in forbdidden_characters:
        parsed_filename = parsed_filename.replace(char, "")

    static_file_path = os.path.join(APP_ROOT, "static", parsed_filename)

    if not os.path.exists(static_file_path):
        return Response(status=404)

    cache_time = int(request.args.get("cache_time", 3600))

    return send_file(path_or_file=static_file_path, max_age=cache_time)
