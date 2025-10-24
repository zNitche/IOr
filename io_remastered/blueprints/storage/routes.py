from flask import Blueprint, redirect, request, flash
from werkzeug.utils import secure_filename
from io_remastered.authentication.decorators import login_required
from io_remastered.io_csrf.decorators import csrf_protected
from io_remastered.consts import DirectoriesConsts
from io_remastered import authentication_manager, models, db, i18n, forms
from io_remastered.types import FlashTypeEnum
from io_remastered.types.action_log_key_enum import ActionLogKeyEnum
from io_remastered.utils import system_logs_utils


storage_blueprint = Blueprint("storage", __name__, template_folder="templates",
                              static_folder="static", url_prefix="/storage")


@storage_blueprint.route("/add-directory", methods=["POST"])
@login_required
@csrf_protected()
def add_directory():
    current_user = authentication_manager.current_user
    form = forms.CreateDirectoryForm(form_data=request.form)

    if form.is_valid():
        dirname = form.get_field_value("name")
        name = secure_filename(filename=dirname if dirname else "")

        if name in DirectoriesConsts.FORBIDDEN_NAMES:
            flash(i18n.t('create_directory_modal.forbidden_name'),
                  FlashTypeEnum.Error.value)

            return redirect(location=request.referrer)

        directory_with_same_name_query = models.Directory.select().filter(
            models.Directory.name == name, models.Directory.owner_id == current_user.id)
        directory_with_same_name = models.Directory.query(
            directory_with_same_name_query).first()

        if directory_with_same_name is None:
            directory = models.Directory(name=name, owner_id=current_user.id)
            db.add(directory)

            flash(i18n.t('create_directory_modal.directory_created'),
                  FlashTypeEnum.Success.value)

            system_logs_utils.log_action(key=ActionLogKeyEnum.DirectoryCreated, metadata={
                "name": directory.name,
                "uuid": directory.uuid
            })

        else:
            flash(i18n.t('create_directory_modal.directory_already_exists', format={"dir_name": name}),
                  FlashTypeEnum.Error.value)

    else:
        flash(i18n.t('create_directory_modal.unexpeted_error'),
              FlashTypeEnum.Error.value)

    return redirect(location=request.referrer)
