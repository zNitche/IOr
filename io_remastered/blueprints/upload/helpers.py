from io_remastered import models, app_helpers
from io_remastered.utils import files_utils


def check_if_files_doesnt_exceed_storage_size(user: models.User, file_size: int):
    user_storage_path = app_helpers.user_storage.get_user_storage_path(user.id)

    user_files_size = files_utils.get_directory_files_size(
        user_storage_path)

    if (user_files_size + file_size) > user.get_max_storage_size_in_bytes():
        return True

    return False
