from io_remastered.io_logging import Logger
from io_remastered.db import Database
from config.app_config import AppConfig


class TaskBase:
    def __init__(self) -> None:
        self.name = self.__class__.__name__
        self.logger = Logger()

        self.db: Database | None = None

    def setup_database(self):
        self.db = Database()
        self.db.setup(db_uri=AppConfig.DATABASE_URI)

        self.db.create_all()

    def setup_logger(self):
        raise NotImplementedError()
    
    def mainloop(self):
        raise NotImplementedError()

    def entrypoint(self):
        self.setup_logger()
        self.setup_database()
        
        self.mainloop()
