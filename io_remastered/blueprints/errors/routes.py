from flask import Blueprint, render_template, redirect, url_for
from io_remastered.blueprints.errors.helpers import headless_error


errors_blueprint = Blueprint("errors", __name__,
                             template_folder="templates", static_folder="static")


@errors_blueprint.app_errorhandler(404)
def error_404(error):
    response = headless_error(error)

    if response:
        return response

    return render_template("error.html", error=error), 404


@errors_blueprint.app_errorhandler(500)
def error_500(error):
    response = headless_error(error)

    if response:
        return response

    return render_template("error.html", error=error), 500


@errors_blueprint.app_errorhandler(405)
def error_405(error):
    response = headless_error(error)

    if response:
        return response

    return render_template("error.html", error=error), 405


@errors_blueprint.app_errorhandler(401)
def error_401(error):
    response = headless_error(error)

    if response:
        return response

    return redirect(url_for("auth.login"))


@errors_blueprint.app_errorhandler(403)
def error_403(error):
    response = headless_error(error)

    if response:
        return response

    return render_template("error.html", error=error), 403
