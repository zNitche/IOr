from typing import Any
import json
from uuid import uuid4


class TaskData:
    def __init__(self, uuid: str, task_name: str, args: str,
                 user_id: str | None = None, is_running: bool = False):

        self.is_running = is_running

        self.user_id = user_id
        self.uuid = uuid
        self.task_name = task_name

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
            "user_id": self.user_id,
            "uuid": self.uuid,
            "task_name": self.task_name,
            "args": self.args,
        }
