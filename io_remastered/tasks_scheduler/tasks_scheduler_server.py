import os
import time
from config.app_config import AppConfig
from io_remastered.io_logging import Logger
from io_remastered.extra_modules import InMemoryDatabase
from io_remastered.db import Database
from io_remastered.tasks_scheduler.tasks import CalcFileChecksumTask
from io_remastered.tasks_scheduler.task_data import TaskData


class TasksSchedulerServer:
    def __init__(self, broker_db: InMemoryDatabase,
                 max_running_tasks: int,
                 mainloop_pooling_interval: int = 5):

        self.__mainloop_pooling_interval = mainloop_pooling_interval

        self.__max_running_tasks = max_running_tasks
        self.__is_running = False

        self.__logger = Logger()

        self.__broker_db = broker_db
        self.__db: Database | None = None

        self.__setup_logger()
        self.__setup_database()

    def __setup_logger(self):
        logs_path = os.path.join("logs", "tasks_scheduler")

        self.__logger.init(logger_name="TasksSchedulerServer", log_to_file=True,
                           logs_filename="tasks_scheduler_server.log", logs_path=logs_path)

    def __setup_database(self):
        self.__db = Database()
        self.__db.setup(db_uri=AppConfig.DATABASE_URI)

        self.__db.create_all()

    def __load_tasks_data(self):
        raw_tasks_uuids = self.__broker_db.get_all_keys_for_pattern("(.*?)")

        queued_tasks: list[TaskData] = []
        running_tasks: list[TaskData] = []

        for task_uuid in raw_tasks_uuids:
            task = self.__broker_db.get_value(task_uuid)

            if not task:
                continue

            task_data = TaskData.from_dict(task)

            if task_data.is_running:
                running_tasks.append(task_data)
            else:
                queued_tasks.append(task_data)

        return queued_tasks, running_tasks

    def __write_tasks_data(self, running_tasks: list[TaskData]):
        for task in running_tasks:
            self.__broker_db.set_value(task.uuid, task.to_dict(), ttl=None)

    def __get_task_for_type(self, task_type: str):
        match task_type:
            case "CALC_FILE_CHECKSUM":
                return CalcFileChecksumTask

        return None

    def __task_keep_alive_callback(self, uuid: str):
        pass

    def __task_on_complete_callback(self, uuid: str):
        self.__broker_db.delete_key(uuid)
        self.__logger.info(f"task {uuid} has been completed")

    def __start_task(self, task: TaskData):
        task_class = self.__get_task_for_type(task.task_type)

        if not task_class:
            raise Exception(f"runner class not found for {task.task_type}")

        t = task_class(uuid=task.uuid, args=task.get_args())
        t.run(db=self.__db, on_complete_callback=self.__task_on_complete_callback,
              task_keep_alive_callback=self.__task_keep_alive_callback)

    def __mainloop(self):
        self.__logger.info("mainloop is running")

        while self.__is_running:
            queued_tasks, running_tasks = self.__load_tasks_data()

            if len(queued_tasks) > 0:
                free_tasks_slots = abs(self.__max_running_tasks - len(running_tasks))

                for _ in range(free_tasks_slots):
                    if len(queued_tasks) == 0:
                        break

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
