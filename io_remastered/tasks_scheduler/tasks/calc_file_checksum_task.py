from typing import Any
from collections.abc import Callable
from io_remastered.tasks_scheduler.tasks.task_base import TaskBase


class CalcFileChecksumTask(TaskBase):
    def __init__(self, uuid: str, args: dict[str, Any]):
        super().__init__(uuid, args)

    def _mainloop(self, on_complete_callback: Callable[[str], None],
                  task_keep_alive_callback: Callable[[str], None]):

        file_uuid = self.args.get("file_uuid")

        print(f"CalcFileChecksumTask -> {file_uuid}")

        task_keep_alive_callback(self.uuid)
        on_complete_callback(self.uuid)