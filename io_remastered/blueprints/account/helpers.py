from io_remastered import models, app_helpers
from io_remastered.types import UserStorageStatistics


def gather_user_storage_stats(user: models.User) -> UserStorageStatistics:
    stats = UserStorageStatistics()

    user_files_query = models.File.select().filter(
        models.File.owner_id == user.id)
    user_dirs_query = models.Directory.select().filter(
        models.Directory.owner_id == user.id)
    
    stats.short_statistics.files = models.File.count(user_files_query)
    stats.short_statistics.directories = models.Directory.count(user_dirs_query)
    stats.short_statistics.shared_files = models.File.count(user_files_query.filter(
        models.File.share_uuid.is_not(None)))  # type: ignore
    stats.short_statistics.shared_directories = models.Directory.count(
        user_dirs_query.filter(models.Directory.share_uuid.is_not(None))) # type: ignore

    files_count_by_extension = {}

    for file in models.File.query(user_files_query).all():
        ext = file.extension

        if ext not in files_count_by_extension.keys():
            files_count_by_extension[ext] = 0

        files_count_by_extension[ext] += 1

    sorted_files_count_by_extension = sorted(
        files_count_by_extension.items(), key=lambda x: x[1])
    sorted_files_count_by_extension.reverse()

    stats.files_count_by_extension = dict(sorted_files_count_by_extension)

    tmp_files_count = len(app_helpers.user_storage.get_user_tmp_files(user.id))
    stats.has_tmp_files = tmp_files_count > 0

    if stats.has_tmp_files:
        stats.short_statistics.tmp_files = tmp_files_count

    return stats
