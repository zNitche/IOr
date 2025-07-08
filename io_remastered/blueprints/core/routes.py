from flask import Blueprint, render_template


core = Blueprint("core", __name__, template_folder="templates", static_folder="static", url_prefix="/")


@core.route("/")
def home():
    return render_template("index.html")
