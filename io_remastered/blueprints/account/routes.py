from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from werkzeug.security import check_password_hash, generate_password_hash
from io_remastered.db.pagination import Pagination, pageable_content
from io_remastered.io_csrf import CSRF, csrf_protected
from io_remastered.authentication.decorators import login_required, password_authentication_required
from io_remastered import authentication_manager, forms, i18n, models, db
from io_remastered.types import FlashTypeEnum
from io_remastered.utils import system_logs_utils


account = Blueprint("account", __name__, template_folder="templates",
                    static_folder="static", url_prefix="/account")


@account.route("", methods=["GET"])
@login_required
def home():
    return render_template("account.html")


@account.route("/change-password", methods=["GET"])
@login_required
def change_password():
    form = forms.ChangePasswordForm(csrf_token=CSRF.generate_token())

    return render_template("change_password.html", form=form)


@account.route("/change-password/submit", methods=["POST"])
@login_required
@csrf_protected()
def handle_change_password():
    form = forms.ChangePasswordForm(form_data=request.form)

    if form.is_valid():
        password = form.get_field_value("password")
        new_password = form.get_field_value("new_password")
        confirm_new_password = form.get_field_value("confirm_password")

        current_user = authentication_manager.current_user

        if not check_password_hash(current_user.password, password):  # type: ignore
            flash(i18n.t("change_password_page.invalid_current_password"),
                  FlashTypeEnum.Error.value)

            system_logs_utils.log_security(
                message_key="password_change_failed")

            return redirect(url_for("account.change_password"))

        if new_password != confirm_new_password:
            flash(i18n.t("change_password_page.passwords_dont_match"),
                  FlashTypeEnum.Error.value)

            return redirect(url_for("account.change_password"))

        user = models.User.query(
            models.User.select().filter_by(id=current_user.id)).first()

        if user:
            user.password = generate_password_hash(
                new_password, salt_length=32)  # type: ignore
            db.commit()

            flash(i18n.t("change_password_page.password_changed_successfully"),
                  FlashTypeEnum.Success.value)

            system_logs_utils.log_security(message_key="password_changed")

    return redirect(url_for("account.change_password"))


@account.route("/sessions", methods=["GET"])
@login_required
def login_sessions():
    current_user = authentication_manager.current_user
    user_sessions = authentication_manager.get_user_sessions(
        user_id=current_user.id)

    return render_template("login_sessions.html", user_sessions=user_sessions)


@account.route("/sessions/<id>/remove", methods=["GET"])
@login_required
@password_authentication_required
def remove_login_sessions(id: str):
    current_user = authentication_manager.current_user
    user_session_for_id = authentication_manager.get_user_session_by_id(
        user_id=current_user.id, id=id)

    if user_session_for_id:
        if user_session_for_id.is_current:
            authentication_manager.logout()

        else:
            authentication_manager.remove_auth_token(
                token=user_session_for_id.key, user_id=current_user.id, via_pattern=False)

            system_logs_utils.log_security(message_key="removed_login_session")

        flash(i18n.t("login_sessions_page.session_removed"),
              FlashTypeEnum.Success.value)

    return redirect(url_for("account.login_sessions"))


@account.route("/storage-statistics", methods=["GET"])
@login_required
def storage_stats():
    current_user = authentication_manager.current_user

    stats = {}

    user_files_query = models.File.select().filter(
        models.File.owner_id == current_user.id)
    user_dirs_query = models.Directory.select().filter(
        models.Directory.owner_id == current_user.id)

    stats["files_count"] = models.File.count(user_files_query)
    stats["directories_count"] = models.Directory.count(user_dirs_query)
    stats["shared_files"] = models.File.count(user_files_query.filter(
        models.File.share_uuid.is_not(None)))  # type: ignore
    stats["shared_directories"] = models.Directory.count(
        user_dirs_query.filter(models.Directory.share_uuid.is_not(None))) # type: ignore

    files_count_by_extension = {}

    for file in models.File.query(user_files_query).all():
        ext = file.extension

        if ext not in files_count_by_extension.keys():
            files_count_by_extension[ext] = 0

        files_count_by_extension[ext] += 1

    sorted_files_count_by_extension = sorted(
        files_count_by_extension.items(), key=lambda x: x[1])
    sorted_files_count_by_extension.reverse()

    stats["files_count_by_extension"] = dict(sorted_files_count_by_extension)

    return render_template("storage_statistics.html", stats=stats)


@account.route("/logs", methods=["GET"])
@login_required
@pageable_content
def logs_preview(page_id: int = 1):
    current_user = authentication_manager.current_user

    logs_query = models.Log.select().filter(
        models.Log.user_id == current_user.id)
    logs_query = logs_query.order_by(models.Log.created_at.desc())

    logs_pagination = Pagination(
        db_model=models.Log,
        query=logs_query,
        page_id=page_id,
        items_per_page=50)

    if not logs_pagination.is_page_id_valid:
        abort(404)

    return render_template("logs_preview.html", logs_pagination=logs_pagination)
