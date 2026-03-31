from typing import Any
from collections.abc import Callable
from threading import Thread
import time


class TaskBase:
    def __init__(self, uuid: str, args: dict[str, Any]):
        self.uuid = uuid
        self.args = args

        self.timestamp = str(time.time())
        self.__thread: Thread | None = None

    def run(self, on_complete_callback: Callable[[str], None],
            task_keep_alive_callback: Callable[[str], None]):

        self.__thread = Thread(target=self._mainloop, args=(
            on_complete_callback, task_keep_alive_callback))
        self.__thread.start()

    def _mainloop(self, on_complete_callback: Callable[[str], None],
                  task_keep_alive_callback: Callable[[str], None]):
        raise NotImplementedError()
