from flask import Blueprint, render_template
from io_remastered.authentication.decorators import login_required
from io_remastered import authentication_manager


account = Blueprint("account", __name__, template_folder="templates",
                    static_folder="static", url_prefix="/account")


@account.route("", methods=["GET"])
@login_required
def home():
    current_user = authentication_manager.current_user
    user_sessions = authentication_manager.get_user_sessions(
        user_id=current_user.id)

    return render_template("account.html", user_sessions=user_sessions)
