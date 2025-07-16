from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash
from io_remastered.io_csrf import CSRF
from io_remastered.io_csrf import csrf_protected
from io_remastered.authentication.decorators import login_required, anonymous_only
from io_remastered import forms, authentication_manager, models


auth = Blueprint("auth", __name__, template_folder="templates",
                 static_folder="static", url_prefix="/auth")


@auth.route("/login", methods=["GET", "POST"])
@anonymous_only
@csrf_protected()
def login():
    form = forms.LoginForm(csrf_token=CSRF.generate_token(), form_data=request.form)

    if form.is_valid():
        username = form.get_field_value("name")
        password = str(form.get_field_value("password"))

        user = models.User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            authentication_manager.login(user.id)

        return redirect(url_for("core.home"))

    return render_template("login.html", form=form)


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    authentication_manager.logout()
    return redirect(url_for("core.home"))
