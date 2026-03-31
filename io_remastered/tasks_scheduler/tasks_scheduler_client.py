from typing import Any
import os
from io_remastered.extra_modules import InMemoryDatabase
from io_remastered.io_logging import Logger
from io_remastered.tasks_scheduler.tasks import TaskTypeEnum
from io_remastered.tasks_scheduler.task_data import TaskData


class TasksSchedulerClient:
    def __init__(self, in_memory_db: InMemoryDatabase):
        self.__logger = Logger()
        self.__in_memory_db = in_memory_db

        self.__setup_logger()

    def __setup_logger(self):
        logs_path = os.path.join("logs", "tasks_scheduler")

        self.__logger.init(logger_name="TasksSchedulerClient", log_to_file=True,
                           logs_filename="tasks_scheduler_client.log", logs_path=logs_path)

    def add_to_queue(self, task_type: TaskTypeEnum, args: dict[str, Any]):
        uuid = TaskData.generate_uuid()
        parsed_args = TaskData.dump_args(args)

        task_data = TaskData(is_running=False, uuid=uuid, task_type=task_type.value,
                             args=parsed_args)

        self.__in_memory_db.set_value(
            key=task_data.uuid, value=task_data.to_dict())

        self.__logger.info(f"{task_data.uuid} added to queue")

    def get_task_status(self):
        pass
