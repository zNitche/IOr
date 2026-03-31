from typing import Any
from threading import Thread
import time

class TaskBase:
    def __init__(self, uuid: str, args: dict[str, Any]):
        self.uuid = uuid
        self.args = args

        self.timestamp = str(time.time())
        self.__thread: Thread | None = None

    def run(self):
        self.__thread = Thread(target=self._mainloop, args=())
        self.__thread.start()

    def _mainloop(self):
        raise NotImplementedError()
