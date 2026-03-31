from typing import Any
import time

class TaskBase:
    def __init__(self, uuid: str, args: dict[str, Any]):
        self.uuid = uuid
        self.arg = args

        self.timestamp = str(time.time())
