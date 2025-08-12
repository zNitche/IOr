import time
from background_tasks.task_base import TaskBase


class FilesCleanupTask(TaskBase):
    def __init__(self):
        super().__init__()

    def mainloop(self):
        time.sleep(1000)
