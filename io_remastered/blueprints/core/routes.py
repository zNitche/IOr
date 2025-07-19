from flask import Blueprint, render_template
from io_remastered.authentication.decorators import login_required


core = Blueprint("core", __name__, template_folder="templates",
                 static_folder="static", url_prefix="/")


@core.route("/")
@login_required
def home():
    return render_template("index.html")
