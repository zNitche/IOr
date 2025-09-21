from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from io_remastered.io_csrf import CSRF, csrf_protected
from io_remastered.authentication.decorators import login_required, anonymous_only
from io_remastered import forms, authentication_manager, models, i18n
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
        password = form.get_field_value("password")

        user = models.User.query(
            models.User.select().filter_by(username=username)).first()

        if user and password and check_password_hash(user.password, password):
            authentication_manager.login(
                user.id, remote_addr=request.remote_addr)

            return redirect(url_for("core.home"))

        else:
            flash(i18n.t("login_page.auth_error"), FlashConsts.TYPE_ERROR)

    return redirect(url_for("auth.login"))


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    authentication_manager.logout()
    return redirect(url_for("core.home"))


@auth.route("/password-authentication", methods=["GET"])
@login_required
def password_authentication():
    origin_url, referrer_url = authentication_manager.get_password_authentication_origin()

    if not origin_url:
        return redirect(url_for("core.home") if not referrer_url else referrer_url)

    form = forms.PasswordAuthenticationForm(csrf_token=CSRF.generate_token())
    return render_template("password_authentication.html", form=form)


@auth.route("/password-authentication/submit", methods=["POST"])
@login_required
def password_authentication_submit():
    origin_url, referrer_url = authentication_manager.get_password_authentication_origin()
    form = forms.PasswordAuthenticationForm(form_data=request.form)

    if form.is_valid():
        password = form.get_field_value("password")
        current_user = authentication_manager.current_user

        if check_password_hash(current_user.password, password):  # type: ignore
            if origin_url:
                authentication_manager.set_last_password_authentication()

                flash(i18n.t("password_authentication_page.auth_success"),
                      FlashConsts.TYPE_SUCCESS)

                return redirect(origin_url)

    flash(i18n.t("password_authentication_page.auth_error"), FlashConsts.TYPE_ERROR)

    return redirect(referrer_url) if referrer_url else redirect(url_for("core.home"))
