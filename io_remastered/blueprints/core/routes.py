from flask import Blueprint, render_template, request, abort
from io_remastered.authentication.decorators import login_required
from io_remastered.io_csrf import csrf_protected, CSRF
from io_remastered import authentication_manager, models, forms
from io_remastered.db.pagination import Pagination
from io_remastered.db.pagination import pageable_content


core = Blueprint("core", __name__, template_folder="templates",
                 static_folder="static", url_prefix="/")


@core.route("/", methods=["GET"])
@login_required
def home():
    current_user = authentication_manager.current_user

    files_query = models.File.select().filter(models.File.owner_id ==
                                              current_user.id).order_by(models.File.upload_date.desc()).limit(20)

    dirs_query = models.Directory.select().filter(models.Directory.owner_id ==
                                                  current_user.id).order_by(models.Directory.created_at.desc()).limit(8)

    files = models.File.query(files_query).all()
    directories = models.Directory.query(dirs_query).all()

    return render_template("index.html", files=files, directories=directories)


@core.route("/files")
@login_required
@pageable_content
def files(page_id: int):
    current_user = authentication_manager.current_user

    search_string = request.args.get("search", "")
    search_form = forms.SearchBarForm(
        form_data={"search-phrase": search_string})

    files_query = models.File.select().filter(models.File.name.icontains(
        search_string), models.File.owner_id ==
        current_user.id).order_by(models.File.upload_date.desc())

    files_pagination = Pagination(
        db_model=models.File, query=files_query, page_id=page_id, items_per_page=3)

    if not files_pagination.is_page_id_valid:
        abort(404)

    return render_template("files.html", files_pagination=files_pagination,
                           files=files_pagination.items, search_form=search_form)

