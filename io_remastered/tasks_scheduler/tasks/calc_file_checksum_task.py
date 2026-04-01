from typing import Any
from collections.abc import Callable
from io_remastered.db import Database
from io_remastered.utils import files_utils
from io_remastered.tasks_scheduler.tasks.task_base import TaskBase


class CalcFileChecksumTask(TaskBase):
    def __init__(self, uuid: str, args: dict[str, Any]):
        super().__init__(uuid, args)

    def _mainloop(self, db: Database | None,
                  on_complete_callback: Callable[[str], None],
                  task_keep_alive_callback: Callable[[str], None]):

        from io_remastered import models

        if db is None:
            raise Exception("")

        file_uuid = self.args.get("file_uuid")
        file_path = self.args.get("target_file_path")

        if not file_uuid or not file_path:
            raise Exception("")

        file = models.File.query(
            models.File.select().filter_by(uuid=file_uuid)).first()

        if not file:
            raise Exception("")

        sha256sum = files_utils.get_sha256sum_for_file(file_path=file_path)
        file.sha256_sum = sha256sum

        db.commit()

        task_keep_alive_callback(self.uuid)
        on_complete_callback(self.uuid)
