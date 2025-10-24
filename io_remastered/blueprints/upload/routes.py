import os
import shutil
import secrets
from uuid import uuid4
from flask import Blueprint, render_template, jsonify, current_app, request, Response
from werkzeug.utils import secure_filename
from io_remastered.authentication.decorators import login_required
from io_remastered.io_csrf.decorators import csrf_protected
from io_remastered import models, authentication_manager, db, i18n
from io_remastered.utils import files_utils, system_logs_utils
from io_remastered.blueprints.upload import helpers
from io_remastered.types import ActionLogKeyEnum


upload = Blueprint("upload", __name__, template_folder="templates",
                   static_folder="static", url_prefix="/upload")


@upload.route("", methods=["GET"])
@login_required
def view():
    return render_template("upload.html")


@upload.route("/preflight", methods=["POST"])
@login_required
@csrf_protected()
def upload_handler_preflight():
    file_size = int(request.headers["X-File-Size"])
    current_user = authentication_manager.current_user

    storage_size_exceeded = helpers.check_if_files_doesnt_exceed_storage_size(
        user=current_user, file_size=file_size)

    if storage_size_exceeded:
        return jsonify({"message": i18n.t("file_upload_backend.messages.storage_size_exceeded")}), 400

    uuid = secrets.token_hex(nbytes=64)
    tmp_files_path = current_app.config["STORAGE_TMP_ROOT_PATH"]

    files_utils.create_tmp_file_for_upload(
        tmp_files_path, uuid, current_user.id)

    return jsonify({"file_uuid": uuid}), 200


@upload.route("/submit", methods=["PUT"])
@login_required
def upload_handler():
    current_user = authentication_manager.current_user

    file_uuid = secure_filename(request.headers["X-File-UUID"])
    req_target_directory_uuid = request.headers.get(
        "X-Target-Directory-UUID", None)

    is_last_chunk = int(request.headers.get("X-Is-Last-Chunk", 0))

    tmp_file_name = files_utils.get_filename_for_tmp_upload(
        uuid=file_uuid, user_id=current_user.id)

    tmp_file_path = os.path.join(
        current_app.config["STORAGE_TMP_ROOT_PATH"], tmp_file_name)

    try:
        files_utils.write_file_from_stream(
            stream=request.stream, file_path=tmp_file_path)

        current_file_size = files_utils.get_file_size(tmp_file_path)

        storage_size_exceeded = helpers.check_if_files_doesnt_exceed_storage_size(
            user=current_user, file_size=current_file_size)

        if storage_size_exceeded:
            return jsonify({"message": i18n.t("file_upload_backend.messages.storage_size_exceeded")}), 400

        if is_last_chunk:
            file_name = secure_filename(request.headers["X-File-Name"])

            if len(file_name) > 64:
                file_name = file_name[:64]

            user_storage_path = os.path.join(
                current_app.config["STORAGE_ROOT_PATH"], str(current_user.id))

            file_uuid = uuid4().hex
            target_file_path = os.path.join(user_storage_path, file_uuid)

            shutil.move(tmp_file_path, target_file_path)

            _, file_extension = os.path.splitext(file_name)
            final_file_size = files_utils.get_file_size(target_file_path)

            sha256sum = files_utils.get_sha256sum_for_file(
                file_path=target_file_path)

            file_object = models.File(uuid=file_uuid, name=file_name,
                                      extension=file_extension, size=final_file_size,
                                      owner_id=current_user.id, sha256_sum=sha256sum)

            if req_target_directory_uuid is not None:
                target_directory = models.Directory.query(
                    models.Directory.select().filter_by(uuid=req_target_directory_uuid,
                                                        owner_id=current_user.id)).first()

                if target_directory is not None:
                    file_object.directory_id = target_directory.id

            db.add(file_object)

            system_logs_utils.log_action(key=ActionLogKeyEnum.FileUploaded, metadata={
                "uuid": file_uuid
            })

            return jsonify({"message": i18n.t("file_upload_backend.messages.uploaded_successfully",
                                              format={"file_name": file_name})}), 200

    except Exception as e:
        current_app.logger.exception(e)

        # cleanup
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)

        return jsonify({"message": i18n.t("file_upload_backend.messages.error_writing_data")}), 500

    return Response(status=200)
