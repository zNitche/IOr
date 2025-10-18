import os
import time
from dataclasses import dataclass
from background_tasks.task_base import TaskBase
from io_remastered import models


@dataclass
class StorageFile:
    path: str
    size: int


class FilesCleanupTask(TaskBase):
    def __init__(self):
        super().__init__()

    def setup_logger(self):
        self.logger.init(logger_name="FilesCleanupTask", log_to_file=True,
                         logs_filename="files_cleanup_task.log", logs_path="logs/")

    def analyze_tmp_files(self):
        storage_tmp_path = os.path.join("files_storage", "tmp")
        files: dict[str, StorageFile] = {}

        for file in os.listdir(storage_tmp_path):
            file_path = os.path.join(storage_tmp_path, file)

            sf = StorageFile(path=file_path,
                             size=os.path.getsize(file_path))
            files[file_path] = sf

        return files

    def process_tmp(self):
        tmp_files_first_pass = self.analyze_tmp_files()
        time.sleep(10)
        tmp_files_second_pass = self.analyze_tmp_files()

        for file_path in tmp_files_first_pass:
            if file_path in tmp_files_second_pass.keys():
                first_check_info = tmp_files_first_pass[file_path]
                second_check_info = tmp_files_second_pass[file_path]

                if first_check_info.size == second_check_info.size:
                    self.logger.info(f"removing tmp file: {file_path}")
                    os.remove(first_check_info.path)

    def get_users_storage_dirs(self, dirs_root_path: str):
        dirs = os.listdir(dirs_root_path)
        filtered_dirs = []

        for dir in dirs:
            try:
                int(dir)
                filtered_dirs.append(dir)

            except:
                pass

        return filtered_dirs

    def analyze_users_storage(self):
        files_info: dict[str, StorageFile] = {}
        dirs_root_path = "./files_storage"
        users_storage_dirs = self.get_users_storage_dirs(dirs_root_path)

        for dir in users_storage_dirs:
            dir_path = os.path.join(dirs_root_path, dir)

            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)
                sf = StorageFile(path=file_path,
                                 size=os.path.getsize(file_path))

                files_info[file] = sf

        return files_info

    def process_users_files(self):
        if self.db is None:
            return

        files_first_pass = self.analyze_users_storage()
        time.sleep(10)
        files_second_pass = self.analyze_users_storage()

        for file_uuid in files_first_pass:
            if file_uuid in files_second_pass.keys():
                first_file_info = files_first_pass[file_uuid]
                second_file_info = files_second_pass[file_uuid]

                if first_file_info.size == second_file_info.size:
                    db_file = models.File.query(
                        models.File.select().filter_by(uuid=file_uuid)).first()

                    if db_file is None:
                        self.logger.info(
                            f"removing user file: {first_file_info.path}")
                        os.remove(first_file_info.path)

    def mainloop(self):
        while True:
            self.process_tmp()
            self.process_users_files()

            time.sleep(60)
