from typing import Any
import time
from io_remastered.tasks_scheduler.tasks.task_base import TaskBase


class CalcFileChecksumTask(TaskBase):
    def __init__(self, uuid: str, args: dict[str, Any]):
        super().__init__(uuid, args)

    def _mainloop(self):
        file_uuid = self.args.get("file_uuid")

        while True:
            print(f"CalcFileChecksumTask -> {file_uuid}")
            time.sleep(1)