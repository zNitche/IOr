from flask import Blueprint, render_template, current_app, Response, request
from io_remastered.csrf_protection import csrf_protected
from io_remastered import forms


core = Blueprint("core", __name__, template_folder="templates", static_folder="static", url_prefix="/")


@core.route("/")
def home():
    current_app.logger.debug("hello world log")
    return render_template("index.html")


@core.route("/csrf-test")
@csrf_protected
def csrf_test():
    return Response(response="ok")


@core.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()

    if request.method == "POST":
        print(request.form.values)

    return render_template("login.html", form=form)
