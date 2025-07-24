from flask import Blueprint, render_template, abort
from io_remastered.authentication.decorators import login_required
from io_remastered import authentication_manager, models


storage = Blueprint("storage", __name__, template_folder="templates",
                  static_folder="static", url_prefix="/storage")


@storage.route("/file/<uuid>", methods=["GET"])
@login_required
def file_preview(uuid: str):
    current_user = authentication_manager.current_user
    file = models.File.query.filter_by(owner_id=current_user.id, uuid=uuid).first()
    
    if not file:
        abort(404)

    return render_template("file_preview.html", file=file)
