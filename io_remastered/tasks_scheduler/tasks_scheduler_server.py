import os
import time
import threading
from io_remastered.io_logging import Logger
from io_remastered.extra_modules import InMemoryDatabase
from io_remastered.tasks_scheduler.tasks import TaskBase
from io_remastered.tasks_scheduler.task_data import TaskData


class TasksSchedulerServer:
    def __init__(self, in_memory_db: InMemoryDatabase,
                 max_running_tasks: int,
                 mainloop_pooling_interval: int = 5):

        self.__mainloop_pooling_interval = mainloop_pooling_interval

        self.__max_running_tasks = max_running_tasks
        self.__is_running = False

        self.__logger = Logger()

        self.__in_memory_db = in_memory_db

        self.__setup_logger()

    def __setup_logger(self):
        logs_path = os.path.join("logs", "tasks_scheduler")

        self.__logger.init(logger_name="TasksSchedulerServer", log_to_file=True,
                           logs_filename="tasks_scheduler_server.log", logs_path=logs_path)

    def __load_tasks_data(self):
        raw_tasks_uuids = self.__in_memory_db.get_all_keys_for_pattern("(.*?)")

        q_tasks: list[TaskData] = []
        r_tasks: list[TaskData] = []

        for task_uuid in raw_tasks_uuids:
            task = self.__in_memory_db.get_value(task_uuid)

            if not task:
                continue

            task_data = TaskData.from_dict(task)

            if task_data.is_running:
                r_tasks.append(task_data)
            else:
                q_tasks.append(task_data)

        return q_tasks, r_tasks

    def __write_tasks_data(self, running_tasks: list[TaskData]):
        for task in running_tasks:
            self.__in_memory_db.set_value(task.uuid, task.to_dict())

    def __start_task(self, task: TaskData):
        pass

    def __mainloop(self):
        self.__logger.info("mainloop is running")

        while self.__is_running:
            queued_tasks, running_tasks = self.__load_tasks_data()

            if len(queued_tasks) > 0:
                if len(running_tasks) < self.__max_running_tasks:
                    task = queued_tasks.pop(0)

                    self.__logger.info(f"starting task {task.uuid}...")

                    task.is_running = True
                    self.__start_task(task)

                    self.__logger.info(f"task {task.uuid} is running")
                    running_tasks.append(task)

                self.__write_tasks_data(running_tasks=running_tasks)

            time.sleep(self.__mainloop_pooling_interval)

        self.__logger.info("mainloop exited")

    def run(self):
        self.__is_running = True

        self.__logger.info("starting mainloop...")
        self.__mainloop()
