from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from io_remastered.io_csrf import CSRF, csrf_protected
from io_remastered.authentication.decorators import login_required, anonymous_only
from io_remastered import forms, authentication_manager, models, i18n
from io_remastered.types import FlashTypeEnum, SecurityLogKeyEnum
from io_remastered.utils import system_logs_utils


auth_blueprint = Blueprint("auth", __name__, template_folder="templates",
                           static_folder="static", url_prefix="/auth")


@auth_blueprint.route("/login", methods=["GET"])
@anonymous_only
def login():
    form = forms.LoginForm(csrf_token=CSRF.generate_token())

    return render_template("login.html", form=form)


@auth_blueprint.route("/login/submit", methods=["POST"])
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

            system_logs_utils.log_security(
                key=SecurityLogKeyEnum.LoggedIn, user_id=user.id)

            return redirect(url_for("core.home"))

        else:
            system_logs_utils.log_security(
                key=SecurityLogKeyEnum.LoginFailed, user_id=user.id if user else None)

            flash(i18n.t("login_page.auth_error"), FlashTypeEnum.Error.value)

    return redirect(url_for("auth.login"))


@auth_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    system_logs_utils.log_security(key=SecurityLogKeyEnum.Logout)

    authentication_manager.logout()
    return redirect(url_for("core.home"))


@auth_blueprint.route("/password-authentication", methods=["GET"])
@login_required
def password_authentication():
    current_user = authentication_manager.current_user
    origin_url, referrer_url = authentication_manager.get_password_authentication_origin()

    if not origin_url:
        return redirect(url_for("core.home") if not referrer_url else referrer_url)

    system_logs_utils.log_security(
        key=SecurityLogKeyEnum.PasswordAuthenticationRequested, user_id=current_user.id, metadata={
            "origin_url": origin_url,
            "referrer_url": referrer_url
        })

    form = forms.PasswordAuthenticationForm(csrf_token=CSRF.generate_token())
    return render_template("password_authentication.html", form=form)


@auth_blueprint.route("/password-authentication/submit", methods=["POST"])
@login_required
def password_authentication_submit():
    origin_url, referrer_url = authentication_manager.get_password_authentication_origin()
    form = forms.PasswordAuthenticationForm(form_data=request.form)

    if form.is_valid():
        password = form.get_field_value("password")
        current_user = authentication_manager.current_user

        if check_password_hash(current_user.password, password):  # type: ignore
            system_logs_utils.log_security(key=SecurityLogKeyEnum.PasswordAuthenticated, metadata={
                "origin_url": origin_url
            })

            if origin_url:
                authentication_manager.set_last_password_authentication()

                flash(i18n.t("password_authentication_page.auth_success"),
                      FlashTypeEnum.Success.value)

                return redirect(origin_url)

        else:
            system_logs_utils.log_security(
                key=SecurityLogKeyEnum.PasswordAuthenticationFailed)

    flash(i18n.t("password_authentication_page.auth_error"),
          FlashTypeEnum.Error.value)

    return redirect(referrer_url) if referrer_url else redirect(url_for("core.home"))
