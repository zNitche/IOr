from io_remastered.db import Database
from io_remastered.utils import files_utils
from io_remastered.tasks_scheduler.tasks.task_base import TaskBase


class CalcFileChecksumTask(TaskBase):
    def _runner(self, db: Database | None):
        from io_remastered import models

        if db is None:
            raise Exception("db is none")

        file_uuid = self.args.get("file_uuid")
        file_path = self.args.get("target_file_path")

        if not file_uuid or not file_path:
            raise Exception("file_uuid and/or file_path is None")

        file = models.File.query(
            models.File.select().filter_by(uuid=file_uuid)).first()

        if not file:
            raise Exception(f"file for uuid {file_uuid} has not been found")

        sha256sum = files_utils.get_sha256sum_for_file(file_path=file_path)
        file.sha256_sum = sha256sum

        db.commit()
