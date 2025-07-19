from flask import Blueprint, render_template
from io_remastered.authentication.decorators import login_required


storage = Blueprint("storage", __name__, template_folder="templates",
                 static_folder="static", url_prefix="/files")


@storage.route("/upload")
@login_required
def file_upload():
    return render_template("upload.html")
