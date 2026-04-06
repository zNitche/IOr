import os
from flask import Blueprint, render_template, abort, send_file, url_for, redirect, request, flash
from io_remastered.authentication.decorators import login_required
from io_remastered.io_csrf.decorators import csrf_protected
from io_remastered import authentication_manager, models, db, i18n, forms, CSRF, tasks_scheduler_client, app_helpers
from io_remastered.types import FlashTypeEnum
from io_remastered.types.action_log_key_enum import ActionLogKeyEnum
from io_remastered.utils import sharing_utils, system_logs_utils, files_utils, requests_utils
from io_remastered.tasks_scheduler.tasks import CalcFileChecksumTask


files_blueprint = Blueprint("files", __name__, template_folder="templates",
                            static_folder="static", url_prefix="/file")


@files_blueprint.route("/<uuid>", methods=["GET"])
@login_required
def preview(uuid: str):
    current_user = authentication_manager.current_user

    file = models.File.query(models.File.select().filter_by(
        uuid=uuid, owner_id=current_user.id)).first()

    if not file:
        abort(404)

    directories = models.Directory.query(models.Directory.select().filter(
        models.Directory.owner_id == current_user.id)).unique().all()

    rename_file_form = forms.RenameStorageItemForm(
        csrf_token=CSRF.generate_token(), name=file.name)

    calc_file_checksum_task_data = tasks_scheduler_client.get_file_task(user_id=current_user.id,
                                                                        task_cls=CalcFileChecksumTask,
                                                                        file_uuid=file.uuid)

    running_scheduled_tasks = {
        "CalcFileChecksumTask": (calc_file_checksum_task_data and calc_file_checksum_task_data.is_running)
    }

    return render_template("file_preview.html",
                           file=file,
                           directories=directories,
                           rename_file_form=rename_file_form,
                           running_scheduled_tasks=running_scheduled_tasks)


@files_blueprint.route("/<uuid>/download", methods=["GET"])
@login_required
def download(uuid: str):
    current_user = authentication_manager.current_user
    file = models.File.query(models.File.select().filter_by(
        uuid=uuid, owner_id=current_user.id)).first()

    if not file:
        abort(404)

    file_path = app_helpers.user_storage.get_file_path(
        file_uuid=file.uuid, user_id=current_user.id)

    filename = file.name if file.name.endswith(
        file.extension) else f"{file.name}{file.extension}"

    return send_file(path_or_file=file_path, as_attachment=True,
                     download_name=filename, max_age=None)


@files_blueprint.route("/<uuid>/remove", methods=["POST"])
@csrf_protected()
@login_required
def remove(uuid: str):
    current_user = authentication_manager.current_user
    file = models.File.query(models.File.select().filter_by(
        owner_id=current_user.id, uuid=uuid)).first()

    if not file:
        abort(404)

    system_logs_utils.log_action(key=ActionLogKeyEnum.FileRemoved, metadata={
        "uuid": file.uuid,
        "filename": file.name
    })

    db.remove(file)

    flash(i18n.t('file_preview_page.file_has_been_removed',
                 format={"uuid": file.uuid, "filename": file.name}),
          FlashTypeEnum.Success.value)

    return redirect(url_for("core.home"))


@files_blueprint.route("/<uuid>/raw-preview", methods=["GET"])
@login_required
def raw_preview(uuid: str):
    current_user = authentication_manager.current_user
    file = models.File.query(models.File.select().filter_by(
        uuid=uuid, owner_id=current_user.id)).first()

    if not file:
        abort(404)

    file_mimetype = files_utils.file_preview_mimetype(file.extension)

    if not file_mimetype:
        abort(404)

    file_path = app_helpers.user_storage.get_file_path(
        file_uuid=file.uuid, user_id=current_user.id)

    range_header = request.headers.get("range")

    if range_header:
        return requests_utils.stream_media_file(range_header=range_header,
                                                file_path=file_path, file_size=file.size,
                                                mimetype=file_mimetype)

    return send_file(path_or_file=file_path, as_attachment=False, mimetype=file_mimetype)


@files_blueprint.route("/<file_uuid>/change-directory", methods=["POST"])
@csrf_protected()
@login_required
def change_directory(file_uuid: str):
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
        file.share_uuid = None

        if directory is not None and directory.is_shared:
            file.share_uuid = sharing_utils.generate_sharing_uuid()

        db.commit()

        flash(i18n.t('change_file_directory.success', format={"dir_name": dir_name}),
              FlashTypeEnum.Success.value)

    else:
        flash(i18n.t('change_file_directory.error'), FlashTypeEnum.Error.value)

    return redirect(location=request.referrer)


@files_blueprint.route("/<uuid>/change-name", methods=["POST"])
@csrf_protected()
@login_required
def change_name(uuid: str):
    current_user = authentication_manager.current_user
    file = models.File.query(models.File.select().filter_by(
        owner_id=current_user.id, uuid=uuid)).first()

    if not file:
        abort(404)

    form = forms.RenameStorageItemForm(name=request.form.get("name"))

    if form.is_valid():
        old_file_name = file.name
        file.name = form.get_field_value("name")

        db.commit()

        flash(i18n.t('change_file_name.success'), FlashTypeEnum.Success.value)

        system_logs_utils.log_action(key=ActionLogKeyEnum.FileRenamed, metadata={
            "uuid": file.uuid,
            "old_name": old_file_name,
            "new_name": file.name
        })

    else:
        flash(i18n.t('change_file_name.error'), FlashTypeEnum.Error.value)

    return redirect(location=request.referrer)


@files_blueprint.route("/<uuid>/recalculate-checksum", methods=["GET"])
@login_required
def recalculate_file_checksum(uuid: str):
    current_user = authentication_manager.current_user
    file = models.File.query(models.File.select().filter_by(
        owner_id=current_user.id, uuid=uuid)).first()

    if not file:
        abort(404)

    file_path = app_helpers.user_storage.get_file_path(
        file_uuid=file.uuid, user_id=current_user.id)

    task_for_file = tasks_scheduler_client.get_file_task(user_id=current_user.id,
                                                         task_cls=CalcFileChecksumTask,
                                                         file_uuid=file.uuid)

    if task_for_file or (task_for_file and task_for_file.is_running):
        flash(i18n.t('recalculate_file_checksum.already_running'),
              FlashTypeEnum.Error.value)

    else:
        try:
            tasks_scheduler_client.add_to_queue(task_cls=CalcFileChecksumTask,
                                                user_id=current_user.id,
                                                args={"file_uuid": file.uuid,
                                                      "target_file_path": file_path})

            flash(i18n.t('recalculate_file_checksum.success'),
                  FlashTypeEnum.Success.value)

        except:
            flash(i18n.t('recalculate_file_checksum.error'),
                  FlashTypeEnum.Error.value)

    return redirect(location=request.referrer)
