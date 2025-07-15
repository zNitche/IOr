from flask import Blueprint, render_template, current_app, Response
from io_remastered.io_csrf import csrf_protected
from io_remastered.authentication.decorators import login_required


core = Blueprint("core", __name__, template_folder="templates",
                 static_folder="static", url_prefix="/")


@core.route("/")
@login_required
def home():
    current_app.logger.debug("hello world log")
    return render_template("index.html")


@core.route("/csrf-test")
@login_required
@csrf_protected()
def csrf_test():
    return Response(response="ok")
