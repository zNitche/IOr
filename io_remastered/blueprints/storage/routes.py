import os
from flask import Blueprint, render_template, abort, send_file, current_app, url_for, redirect, request, flash
from io_remastered.authentication.decorators import login_required
from io_remastered.io_csrf.decorators import csrf_protected
from io_remastered import authentication_manager, models, db, i18n
from io_remastered.consts import FlashConsts


storage = Blueprint("storage", __name__, template_folder="templates",
                    static_folder="static", url_prefix="/storage")


@storage.route("/file/<uuid>", methods=["GET"])
@login_required
def file_preview(uuid: str):
    current_user = authentication_manager.current_user

    file = models.File.query(models.File.select().filter_by(
        owner_id=current_user.id, uuid=uuid)).first()

    if not file:
        abort(404)

    directories = models.Directory.query(models.Directory.select().filter(
        models.Directory.owner_id == current_user.id)).unique().all()

    return render_template("file_preview.html", file=file, directories=directories)


@storage.route("/file/<uuid>/download", methods=["GET"])
@login_required
def download_file(uuid: str):
    current_user = authentication_manager.current_user
    file = models.File.query(models.File.select().filter_by(
        owner_id=current_user.id, uuid=uuid)).first()

    if not file:
        abort(404)

    user_storage_path = os.path.join(
        current_app.config["STORAGE_ROOT_PATH"], str(current_user.id))

    file_path = os.path.join(user_storage_path, file.uuid)

    return send_file(path_or_file=file_path, as_attachment=True,
                     download_name=file.name, max_age=None)


@storage.route("/file/<uuid>/remove", methods=["POST"])
@csrf_protected()
@login_required
def remove_file(uuid: str):
    current_user = authentication_manager.current_user
    file = models.File.query(models.File.select().filter_by(
        owner_id=current_user.id, uuid=uuid)).first()

    if not file:
        abort(404)

    db.remove(file)

    return redirect(url_for("core.home"))


@storage.route("/file/<file_uuid>/change-directory", methods=["POST"])
@csrf_protected()
@login_required
def change_file_directory(file_uuid: str):
    current_user = authentication_manager.current_user
    file = models.File.query(models.File.select().filter_by(
        owner_id=current_user.id, uuid=file_uuid)).first()

    if not file:
        abort(404)

    selected_directory_uuid = request.form.get("new-directory")

    directory = models.Directory.query(models.Directory.select().filter_by(
        owner_id=current_user.id, uuid=selected_directory_uuid)).first()

    if selected_directory_uuid == "/" or directory is not None:
        dir_name = directory.name if directory is not None else "/"

        file.directory_id = directory.id if directory is not None else None
        db.commit()

        flash(i18n.t('change_file_directory.success', format={"dir_name": dir_name}),
              FlashConsts.TYPE_SUCCESS)

    else:
        flash(i18n.t('change_file_directory.error'), FlashConsts.TYPE_ERROR)

    return redirect(location=request.referrer)


@storage.route("/directory/<uuid>", methods=["GET"])
@login_required
def directory_preview(uuid: str):
    current_user = authentication_manager.current_user

    directory = models.Directory.query(models.Directory.select().filter_by(
        owner_id=current_user.id, uuid=uuid)).first()

    if not directory:
        abort(404)

    return render_template("directory_preview.html", directory=directory)
