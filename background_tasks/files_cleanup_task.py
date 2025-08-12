from background_tasks.task_base import TaskBase


class FilesCleanupTask(TaskBase):
    def __init__(self) -> None:
        super().__init__()
