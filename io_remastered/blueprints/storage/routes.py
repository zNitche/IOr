from flask import Blueprint, render_template, Response
from io_remastered.authentication.decorators import login_required
from io_remastered.io_csrf.decorators import csrf_protected


storage = Blueprint("storage", __name__, template_folder="templates",
                 static_folder="static", url_prefix="/files")


@storage.route("/upload", methods=["GET"])
@login_required
def upload():
    return render_template("upload.html")


@storage.route("/upload/submit", methods=["POST"])
@login_required
@csrf_protected()
def upload_handler():
    return Response(), 200
