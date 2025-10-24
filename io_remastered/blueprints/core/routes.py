from flask import Blueprint, render_template, request, abort
from io_remastered.authentication.decorators import login_required
from io_remastered.io_csrf import CSRF
from io_remastered import authentication_manager, models, forms
from io_remastered.db.pagination import Pagination, pageable_content


core_blueprint = Blueprint("core", __name__, template_folder="templates",
                 static_folder="static", url_prefix="/")


@core_blueprint.route("", methods=["GET"])
@login_required
def home():
    current_user = authentication_manager.current_user

    files_query = models.File.select().filter(models.File.owner_id ==
                                              current_user.id).order_by(models.File.upload_date.desc()).limit(20)

    dirs_query = models.Directory.select().filter(models.Directory.owner_id ==
                                                  current_user.id).order_by(models.Directory.created_at.desc()).limit(8)

    files = models.File.query(files_query).all()
    directories = models.Directory.query(dirs_query).unique().all()

    return render_template("home.html", files=files, directories=directories)


@core_blueprint.route("/files")
@login_required
@pageable_content
def files(page_id: int):
    current_user = authentication_manager.current_user

    only_shared = int(request.args.get("only_shared", 0))
    search_string = request.args.get("search", "")

    search_form = forms.SearchBarForm(search_phrase=search_string)

    files_query = models.File.select().filter(models.File.name.icontains(
        search_string), models.File.owner_id == current_user.id)

    if only_shared:
        files_query = files_query.filter(
            models.File.share_uuid.is_not(None))  # type: ignore

    files_query = files_query.order_by(models.File.upload_date.desc())

    files_pagination = Pagination(
        db_model=models.File, query=files_query, page_id=page_id)

    if not files_pagination.is_page_id_valid:
        abort(404)

    return render_template("files.html", files_pagination=files_pagination,
                           files=files_pagination.items, search_form=search_form,
                           only_shared=only_shared)


@core_blueprint.route("/directories", methods=["GET"])
@login_required
@pageable_content
def directories(page_id: int):
    current_user = authentication_manager.current_user

    only_shared = int(request.args.get("only_shared", 0))
    search_string = request.args.get("search", "")

    search_form = forms.SearchBarForm(search_phrase=search_string)

    dirs_query = models.Directory.select().filter(models.Directory.name.icontains(
        search_string), models.Directory.owner_id == current_user.id)

    if only_shared:
        dirs_query = dirs_query.filter(
            models.Directory.share_uuid.is_not(None))  # type: ignore

    dirs_query = dirs_query.order_by(models.Directory.created_at.desc())

    directories_pagination = Pagination(
        db_model=models.Directory, query=dirs_query, page_id=page_id)

    if not directories_pagination.is_page_id_valid:
        abort(404)

    create_directory_form = forms.CreateDirectoryForm(
        csrf_token=CSRF.generate_token())

    return render_template("directories.html",
                           directories_pagination=directories_pagination,
                           directories=directories_pagination.items,
                           search_form=search_form,
                           create_directory_form=create_directory_form,
                           only_shared=only_shared)
