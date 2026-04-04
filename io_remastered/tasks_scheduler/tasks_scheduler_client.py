from typing import Any
import os
from io_remastered.extra_modules import InMemoryDatabase
from io_remastered.io_logging import Logger
from io_remastered.tasks_scheduler.task_data import TaskData
from io_remastered.tasks_scheduler.tasks import TaskBase


class TasksSchedulerClient:
    def __init__(self, broker_db: InMemoryDatabase):
        self.__logger = Logger()
        self.__broker_db = broker_db

        self.__setup_logger()

    def __setup_logger(self):
        logs_path = os.path.join("logs", "tasks_scheduler")

        self.__logger.init(logger_name="TasksSchedulerClient", log_to_file=True,
                           logs_filename="tasks_scheduler_client.log", logs_path=logs_path,
                           backup_log_files_count=1)

    def add_to_queue(self, task_cls: type[TaskBase], args: dict[str, Any],
                     user_id: str | None = None):

        uuid = TaskData.generate_uuid()
        parsed_args = TaskData.dump_args(args)

        task_data = TaskData(uuid=uuid,
                             task_name=task_cls.get_name(),
                             args=parsed_args, user_id=user_id)

        self.__broker_db.set_value(
            key=task_data.uuid, value=task_data.to_dict(), ttl=None)

        self.__logger.info(f"{task_data.uuid} added to queue")

    def check_if_task_is_running(self, task_uuid: str):
        raw_task_data = self.__broker_db.get_value(task_uuid)

        if not raw_task_data:
            return False

        task_data = TaskData.from_dict(raw_task_data)

        return task_data.is_running
    
    def check_if_task_is_in_queue(self, task_uuid: str):
        raw_task_data = self.__broker_db.get_value(task_uuid)

        if not raw_task_data:
            return False

        task_data = TaskData.from_dict(raw_task_data)

        return not task_data.is_running

    def get_file_task(self, user_id: str, task_cls: type[TaskBase], file_uuid: str):
        raw_tasks_uuids = self.__broker_db.get_all_keys_for_pattern("(.*?)")

        for task_uuid in raw_tasks_uuids:
            task = self.__broker_db.get_value(task_uuid)

            if not task:
                continue

            task_data = TaskData.from_dict(task)

            if task_data.user_id != user_id:
                continue

            if task_data.task_name != task_cls.get_name():
                continue

            task_args = task_data.get_args()

            if task_args.get("file_uuid") == file_uuid:
                return task_data

        return None
