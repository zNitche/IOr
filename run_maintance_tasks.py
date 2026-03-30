import multiprocessing
from io_remastered.io_logging import Logger
from maintenance_tasks import TaskBase, FilesCleanupTask, UsersSecurityLogsCleanupTask


class MaintenanceTasksRunner:
    def __init__(self) -> None:
        self.logger = Logger()

        self.setup_logger()

    def setup_logger(self):
        self.logger.init(logger_name="MaintenanceTasksRunner", log_to_file=True,
                         logs_filename="maintenance_tasks_runner.log", logs_path="logs/")

    def get_tasks(self) -> list[type[TaskBase]]:
        return [FilesCleanupTask, UsersSecurityLogsCleanupTask]

    def run(self):
        self.logger.info("starting maintenance tasks...")
        tasks = self.get_tasks()

        self.logger.info(f"{len(tasks)} task(s) has been found, processing...")

        for task_class in tasks:
            task_instance = task_class()

            try:
                self.logger.info(f"starting {task_instance.name}...")

                process = multiprocessing.Process(
                    target=task_instance.entrypoint)
                process.start()

                self.logger.info(f"{task_instance.name} has been started")

            except Exception as e:
                self.logger.exception(
                    f"an exception occured while starting {task_instance.name}: {str(e)}")

        self.logger.info("done")


if __name__ == "__main__":
    runner = MaintenanceTasksRunner()
    runner.run()
