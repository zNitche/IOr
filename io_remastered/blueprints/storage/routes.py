import os
from flask import Blueprint, render_template, abort, send_file, current_app, \
    url_for, redirect, request, flash
from io_remastered.authentication.decorators import login_required
from io_remastered.io_csrf.decorators import csrf_protected
from io_remastered.consts import DirectoriesConsts
from io_remastered import authentication_manager, models, db, i18n, forms, CSRF
from io_remastered.db.pagination import Pagination, pageable_content
from io_remastered.types import FlashTypeEnum
from io_remastered.utils import sharing_utils, requests_utils


storage = Blueprint("storage", __name__, template_folder="templates",
                    static_folder="static", url_prefix="/storage")


@storage.route("/file/<uuid>", methods=["GET"])
@login_required
def file_preview(uuid: str):
    current_user = authentication_manager.current_user

    file = models.File.query(models.File.select().filter_by(
        uuid=uuid, owner_id=current_user.id)).first()

    if not file:
        abort(404)

    directories = models.Directory.query(models.Directory.select().filter(
        models.Directory.owner_id == current_user.id)).unique().all()

    rename_file_form = forms.RenameStorageItemForm(
        csrf_token=CSRF.generate_token(), name=file.name)

    return render_template("file_preview.html",
                           file=file,
                           directories=directories,
                           rename_file_form=rename_file_form)


@storage.route("/file/<uuid>/download", methods=["GET"])
@login_required
def download_file(uuid: str):
    current_user = authentication_manager.current_user
    file = models.File.query(models.File.select().filter_by(
        uuid=uuid, owner_id=current_user.id)).first()

    if not file:
        abort(404)

    user_storage_path = os.path.join(
        current_app.config["STORAGE_ROOT_PATH"], str(file.owner_id))

    file_path = os.path.join(user_storage_path, file.uuid)
    filename = file.name if file.name.endswith(
        file.extension) else f"{file.name}{file.extension}"

    return send_file(path_or_file=file_path, as_attachment=True,
                     download_name=filename, max_age=None)


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
        file.share_uuid = None

        if directory is not None and directory.is_shared:
            file.share_uuid = sharing_utils.generate_sharing_uuid()

        db.commit()

        flash(i18n.t('change_file_directory.success', format={"dir_name": dir_name}),
              FlashTypeEnum.Success.value)

    else:
        flash(i18n.t('change_file_directory.error'), FlashTypeEnum.Error.value)

    return redirect(location=request.referrer)


@storage.route("/file/<uuid>/change-name", methods=["POST"])
@csrf_protected()
@login_required
def change_file_name(uuid: str):
    current_user = authentication_manager.current_user
    file = models.File.query(models.File.select().filter_by(
        owner_id=current_user.id, uuid=uuid)).first()

    if not file:
        abort(404)

    form = forms.RenameStorageItemForm(name=request.form.get("name"))

    if form.is_valid():
        file.name = form.get_field_value("name")

        db.commit()

        flash(i18n.t('change_file_name.success'), FlashTypeEnum.Success.value)

    else:
        flash(i18n.t('change_file_name.error'), FlashTypeEnum.Error.value)

    return redirect(location=request.referrer)


@storage.route("/directory/<uuid>", methods=["GET"])
@login_required
@pageable_content
def directory_preview(page_id: int, uuid: str):
    current_user = authentication_manager.current_user

    directory = models.Directory.query(
        models.Directory.select().filter_by(uuid=uuid, owner_id=current_user.id)).first()

    if not directory:
        abort(404)

    search_string = request.args.get("search", "")
    search_form = forms.SearchBarForm(search_phrase=search_string)

    files_query = models.File.select().filter(models.File.name.icontains(search_string),
                                              models.File.owner_id == current_user.id,
                                              models.File.directory_id == directory.id).order_by(models.File.upload_date.desc())

    files_pagination = Pagination(
        db_model=models.File, query=files_query, page_id=page_id)

    if not files_pagination.is_page_id_valid:
        abort(404)

    rename_directory_form = forms.RenameStorageItemForm(
        csrf_token=CSRF.generate_token(), name=directory.name)

    return render_template("directory_preview.html",
                           directory=directory,
                           search_form=search_form,
                           files_pagination=files_pagination,
                           rename_directory_form=rename_directory_form)


@storage.route("/directory/<uuid>/remove", methods=["POST"])
@csrf_protected()
@login_required
def remove_directory(uuid: str):
    current_user = authentication_manager.current_user
    directory = models.Directory.query(models.Directory.select().filter_by(
        owner_id=current_user.id, uuid=uuid)).first()

    if not directory:
        abort(404)

    remove_all_directory_files = request.form.get("remove-all-files") == "on"

    if remove_all_directory_files:
        for file in directory.files:
            db.remove(file)

    db.remove(directory)

    flash(i18n.t('remove_directory.success'), FlashTypeEnum.Success.value)

    return redirect(url_for("core.home"))


@storage.route("/directory/<uuid>/download", methods=["GET"])
@login_required
def download_directory(uuid: str):
    current_user = authentication_manager.current_user
    directory = models.Directory.query(models.Directory.select().filter_by(
        owner_id=current_user.id, uuid=uuid)).first()

    if not directory:
        abort(404)

    user_storage_path = os.path.join(
        current_app.config["STORAGE_ROOT_PATH"], str(current_user.id))

    return requests_utils.send_directory_as_zip(directory=directory,
                                                user_storage_path=user_storage_path)


@storage.route("/directory/<uuid>/change-name", methods=["POST"])
@csrf_protected()
@login_required
def change_directory_name(uuid: str):
    current_user = authentication_manager.current_user
    directory = models.Directory.query(models.Directory.select().filter_by(
        owner_id=current_user.id, uuid=uuid)).first()

    if not directory:
        abort(404)

    form = forms.RenameStorageItemForm(name=request.form.get("name"))

    if form.is_valid():
        directory_name = form.get_field_value("name")

        if directory_name not in DirectoriesConsts.FORBIDDEN_NAMES:
            directory.name = directory_name
            db.commit()

            flash(i18n.t('change_directory_name.success'),
                  FlashTypeEnum.Success.value)

        else:
            flash(i18n.t('create_directory_modal.forbidden_name'),
                  FlashTypeEnum.Error.value)

    else:
        flash(i18n.t('change_directory_name.error'), FlashTypeEnum.Error.value)

    return redirect(location=request.referrer)


@storage.route("/directory/<directory_uuid>/toggle-sharing", methods=["POST"])
@csrf_protected()
@login_required
def toggle_directory_sharing(directory_uuid: str):
    current_user = authentication_manager.current_user
    directory = models.Directory.query(models.Directory.select().filter_by(
        owner_id=current_user.id, uuid=directory_uuid)).first()

    if not directory:
        abort(404)

    next_state = not directory.is_shared

    directory.toggle_sharing(state=next_state)
    db.commit()

    flash(i18n.t(f'toggle_directory_sharing.{'disabled' if not next_state else "enabled"}'),
          FlashTypeEnum.Success.value)

    return redirect(location=request.referrer)
