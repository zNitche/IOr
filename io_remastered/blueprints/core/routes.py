from flask import Blueprint, render_template, request, abort, redirect, flash
from werkzeug.utils import secure_filename
from io_remastered.authentication.decorators import login_required
from io_remastered.consts import FlashConsts
from io_remastered.io_csrf import csrf_protected, CSRF
from io_remastered import authentication_manager, models, forms, i18n, db
from io_remastered.db.pagination import Pagination, pageable_content


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
    directories = models.Directory.query(dirs_query).unique().all()

    return render_template("home.html", files=files, directories=directories)


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
        db_model=models.File, query=files_query, page_id=page_id)

    if not files_pagination.is_page_id_valid:
        abort(404)

    return render_template("files.html", files_pagination=files_pagination,
                           files=files_pagination.items, search_form=search_form)


@core.route("/directories", methods=["GET"])
@login_required
@pageable_content
def directories(page_id: int):
    current_user = authentication_manager.current_user

    search_string = request.args.get("search", "")
    search_form = forms.SearchBarForm(
        form_data={"search-phrase": search_string})

    dirs_query = models.Directory.select().filter(models.Directory.name.icontains(
        search_string), models.Directory.owner_id ==
        current_user.id).order_by(models.Directory.created_at.desc())

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
                           create_directory_form=create_directory_form)


@core.route("/add-directory", methods=["POST"])
@login_required
@csrf_protected()
def add_directory():
    current_user = authentication_manager.current_user
    form = forms.CreateDirectoryForm(form_data=request.form)

    if form.is_valid():
        dirname = form.get_field_value("name")
        name = secure_filename(filename=dirname if dirname else "")

        directory = models.Directory(name=name, owner_id=current_user.id)
        db.add(directory)

        flash(i18n.t('create_directory_modal.directory_created'),
              FlashConsts.TYPE_SUCCESS)

    else:
        flash(i18n.t('create_directory_modal.unexpeted_error'),
              FlashConsts.TYPE_ERROR)

    return redirect(location=request.referrer)
