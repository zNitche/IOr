import os
from flask import current_app
from io_remastered import authentication_manager
from io_remastered.utils import files_utils


def get_taken_storage():
    user = authentication_manager.current_user

    storage_path = current_app.config["STORAGE_ROOT_PATH"]
    user_storage_path = os.path.join(storage_path, str(user.id))

    user_taken_space = files_utils.get_directory_files_size(user_storage_path)

    return round(user_taken_space / 1_000_000_000, 2)
