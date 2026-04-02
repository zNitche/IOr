from typing import Any
from collections.abc import Callable
from threading import Thread
from io_remastered.db import Database
import time


class TaskBase:
    def __init__(self, uuid: str, args: dict[str, Any]):
        self.uuid = uuid
        self.args = args

        self.timestamp = str(time.time())
        self.__thread: Thread | None = None

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
            pass

        on_complete_callback(self.uuid)

    def _runner(self, db: Database | None):
         raise NotImplementedError()
