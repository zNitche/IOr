from flask import Blueprint, redirect, url_for, Response


errors = Blueprint("errors", __name__, template_folder="templates", static_folder="static")


@errors.app_errorhandler(401)
def error_401(error):
    return redirect(url_for("auth.login"))
