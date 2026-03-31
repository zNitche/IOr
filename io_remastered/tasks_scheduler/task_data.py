from typing import Any
import json
from uuid import uuid4


class TaskData:
    def __init__(self, is_running: bool, uuid: str, task_type: str, args: str):
        self.is_running = is_running
        self.uuid = uuid
        self.task_type = task_type
        self.args = args

    def get_args(self):
        return json.loads(self.args)
    
    @staticmethod
    def dump_args(args: dict[str, Any]):
        return json.dumps(args)

    @staticmethod
    def from_dict(data: dict):
        return TaskData(**data)

    @staticmethod
    def generate_uuid():
        return uuid4().hex

    def to_dict(self):
        return {
            "is_running": self.is_running,
            "uuid": self.uuid,
            "task_type": self.task_type,
            "args": self.args,
        }
