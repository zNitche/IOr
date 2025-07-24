import os
from flask import current_app
from io_remastered import models
from io_remastered.utils import files_utils


def check_if_files_doesnt_exceed_storage_size(user: models.User, file_size: int):
    user_storage_path = os.path.join(
        current_app.config["STORAGE_ROOT_PATH"], str(user.id))
    user_files_size = files_utils.get_directory_files_size(user_storage_path)

    if (user_files_size + file_size) > user.get_max_storage_size_in_bytes():
        return True

    return False
