import os
from flask import Blueprint, render_template, abort, send_file, current_app
from io_remastered.authentication.decorators import login_required
from io_remastered import authentication_manager, models


storage = Blueprint("storage", __name__, template_folder="templates",
                    static_folder="static", url_prefix="/storage")


@storage.route("/file/<uuid>", methods=["GET"])
@login_required
def file_preview(uuid: str):
    current_user = authentication_manager.current_user
    file = models.File.query.filter_by(
        owner_id=current_user.id, uuid=uuid).first()

    if not file:
        abort(404)

    return render_template("file_preview.html", file=file)


@storage.route("/file/<uuid>/download", methods=["GET"])
@login_required
def download_file(uuid: str):
    current_user = authentication_manager.current_user
    file = models.File.query.filter_by(
        owner_id=current_user.id, uuid=uuid).first()

    if not file:
        abort(404)

    user_storage_path = os.path.join(
        current_app.config["STORAGE_ROOT_PATH"], str(current_user.id))

    file_path = os.path.join(user_storage_path, file.uuid)

    return send_file(path_or_file=file_path, as_attachment=True,
                     download_name=file.name, max_age=None)
