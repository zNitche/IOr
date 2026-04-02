import time
import os
from typing import Any
from collections.abc import Callable
from threading import Thread
from io_remastered.db import Database
from io_remastered.io_logging import Logger


class TaskBase:
    def __init__(self, uuid: str, args: dict[str, Any]):
        self.uuid = uuid
        self.args = args

        self.timestamp = str(time.time())
        self.__thread: Thread | None = None

        self.logger = self.__get_logger()

    def __get_logger(self):
        return Logger.get_expandable_logger(
            logger_name="ScheduledTask",
            extra={"uuid": self.uuid},
            logs_path=os.path.join("logs", "tasks_scheduler", "tasks"),
            logs_filename="scheduled_task.log",
            backup_log_files_count=1)

    @classmethod
    def get_name(cls):
        return cls.__class__.__name__

    def run(self, db: Database | None, on_complete_callback: Callable[[str], None]):
        self.__thread = Thread(target=self.__mainloop,
                               args=(db, on_complete_callback))
        self.__thread.start()

    def __mainloop(self, db: Database | None, on_complete_callback: Callable[[str], None]):
        try:
            self._runner(db=db)

        except:
            self.logger.exception(
                f"exception while running {self.__class__.__name__} [{self.uuid}] , with args: {self.args}")

        on_complete_callback(self.uuid)

    def _runner(self, db: Database | None):
        raise NotImplementedError()
