from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from io_remastered.io_csrf import CSRF, csrf_protected
from io_remastered.authentication.decorators import login_required, anonymous_only
from io_remastered import forms, authentication_manager, models
from io_remastered.consts import FlashConsts


auth = Blueprint("auth", __name__, template_folder="templates",
                 static_folder="static", url_prefix="/auth")


@auth.route("/login", methods=["GET"])
@anonymous_only
def login():
    form = forms.LoginForm(csrf_token=CSRF.generate_token())

    return render_template("login.html", form=form)


@auth.route("/login/submit", methods=["POST"])
@anonymous_only
@csrf_protected()
def login_submit():
    form = forms.LoginForm(form_data=request.form)

    if form.is_valid():
        username = form.get_field_value("name")
        password = str(form.get_field_value("password"))

        user = models.User.query(
            models.User.select().filter_by(username=username)).first()

        if user and check_password_hash(user.password, password):
            authentication_manager.login(user.id)

            return redirect(url_for("core.home"))

        else:
            flash("wrong name or password", FlashConsts.TYPE_ERROR)

    return redirect(url_for("auth.login"))


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    authentication_manager.logout()
    return redirect(url_for("core.home"))
