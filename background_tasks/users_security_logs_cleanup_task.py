import time
from datetime import datetime
from io_remastered.models import UserSecurityLog
from background_tasks import TaskBase

class UsersSecurityLogsCleanupTask(TaskBase):
    def __init__(self):
        super().__init__()

    def setup_logger(self):
        self.logger.init(logger_name="UsersSecurityLogsCleanupTask", log_to_file=True,
                         logs_filename="users_security_logs_cleanup_task.log", logs_path="logs/")
    
    def mainloop(self):
        if not self.db:
            self.logger.error("db is None, skipping...")

            return

        date_now = datetime.now()

        try:
            users_security_logs = UserSecurityLog.query(UserSecurityLog.select()).all()
            logs_count = UserSecurityLog.count(UserSecurityLog.select())

            self.logger.info(f"checking, found: {logs_count} logs...")

            removed_logs_count = 0

            for log in users_security_logs:
                time_difference = date_now - log.created_at

                if time_difference.days >= 28:
                    self.db.remove(log, commit_on_completion=False)
                    removed_logs_count += 1

            self.db.commit()

            self.logger.info(f"removed {removed_logs_count} logs")

        except:
            self.logger.exception("an exception occured while processing mainloop")

        self.logger.info("done, sleeping.")

        # every 6 hours
        time.sleep(3600 * 6)
