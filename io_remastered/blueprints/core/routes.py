from flask import Blueprint, render_template, current_app, Response, request
from io_remastered.csrf_protection import csrf_protected, CSRF
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


@core.route("/login", methods=["GET"])
def login_view():
    form = forms.LoginForm(csrf_token=CSRF.generate_token())

    return render_template("login.html", form=form)


@core.route("/login/action", methods=["POST"])
@csrf_protected
def login_action():
    form = forms.LoginForm()

    print(request.form.values)

    return "ok"
