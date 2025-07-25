from flask import Blueprint, render_template, request
from io_remastered.authentication.decorators import login_required
from io_remastered import authentication_manager, forms, models


core = Blueprint("core", __name__, template_folder="templates",
                 static_folder="static", url_prefix="/")


@core.route("/", methods=["GET"])
@login_required
def home():
    current_user = authentication_manager.current_user

    search_string = request.args.get("search", "")
    form = forms.SearchBarForm(form_data={"search-phrase": search_string})

    files_query = models.File.select().filter(models.File.name.icontains(
        search_string), models.File.owner_id == current_user.id).order_by(models.File.upload_date.desc())

    files = models.File.query(files_query).all()
    files_count = models.File.count(files_query)

    return render_template("index.html", files=files, form=form, files_count=files_count)
