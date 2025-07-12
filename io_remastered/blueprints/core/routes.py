from flask import Blueprint, render_template, current_app
from io_remastered.csrf_protection import csrf_protected


core = Blueprint("core", __name__, template_folder="templates", static_folder="static", url_prefix="/")


@core.route("/")
def home():
    current_app.logger.debug("hello world log")
    return render_template("index.html")


@core.route("/csrf-test")
@csrf_protected
def csrf_test():
    return render_template("index.html")
