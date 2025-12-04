import os
from flask import Blueprint, render_template, abort, send_file, current_app, request
from io_remastered import models, forms
from io_remastered.utils import requests_utils, files_utils
from io_remastered.db.pagination import Pagination, pageable_content


share_blueprint = Blueprint("share", __name__, template_folder="templates",
                            static_folder="static", url_prefix="/share")


@share_blueprint.route("/file/<share_uuid>", methods=["GET"])
def file_preview(share_uuid: str):
    file = models.File.query(models.File.select().filter_by(
        share_uuid=share_uuid)).first()

    if not file:
        abort(404)

    return render_template("shared_file_preview.html", file=file)


@share_blueprint.route("/<share_uuid>/raw-preview", methods=["GET"])
def file_raw_preview(share_uuid: str):
    file = models.File.query(models.File.select().filter_by(
        share_uuid=share_uuid)).first()

    if not file:
        abort(404)

    file_mimetype = files_utils.file_preview_mimetype(file.extension)

    if not file_mimetype:
        abort(404)

    user_storage_path = os.path.join(
        current_app.config["STORAGE_ROOT_PATH"], str(file.owner_id))

    file_path = os.path.join(user_storage_path, file.uuid)

    range_header = request.headers.get("range")

    if range_header:
        return requests_utils.stream_media_file(range_header=range_header,
                                                file_path=file_path, file_size=file.size,
                                                mimetype=file_mimetype)

    return send_file(path_or_file=file_path, as_attachment=False, mimetype=file_mimetype)


@share_blueprint.route("/file/<share_uuid>/download", methods=["GET"])
def download_file(share_uuid: str):
    file = models.File.query(models.File.select().filter_by(
        share_uuid=share_uuid)).first()

    if not file:
        abort(404)

    user_storage_path = os.path.join(
        current_app.config["STORAGE_ROOT_PATH"], str(file.owner_id))

    file_path = os.path.join(user_storage_path, file.uuid)
    filename = file.name if file.name.endswith(
        file.extension) else f"{file.name}{file.extension}"

    return send_file(path_or_file=file_path, as_attachment=True,
                     download_name=filename, max_age=None)


@share_blueprint.route("/directory/<share_uuid>", methods=["GET"])
@pageable_content
def directory_preview(page_id: int, share_uuid: str):
    directory = models.Directory.query(
        models.Directory.select().filter_by(share_uuid=share_uuid)).first()

    if not directory:
        abort(404)

    search_string = request.args.get("search", "")
    search_form = forms.SearchBarForm(search_phrase=search_string)

    files_query = models.File.select().filter(models.File.name.icontains(search_string),
                                              models.File.directory_id == directory.id,
                                              models.File.share_uuid.is_not(None)).order_by(models.File.upload_date.desc())

    files_pagination = Pagination(
        db_model=models.File, query=files_query, page_id=page_id)

    if not files_pagination.is_page_id_valid:
        abort(404)

    return render_template("shared_directory_preview.html",
                           directory=directory,
                           search_form=search_form,
                           files_pagination=files_pagination)


@share_blueprint.route("/directory/<share_uuid>/download", methods=["GET"])
def download_directory(share_uuid: str):
    directory = models.Directory.query(
        models.Directory.select().filter_by(share_uuid=share_uuid)).first()

    if not directory:
        abort(404)

    user_storage_path = os.path.join(
        current_app.config["STORAGE_ROOT_PATH"], str(directory.owner_id))

    return requests_utils.send_directory_as_zip(directory=directory,
                                                user_storage_path=user_storage_path)
