import logging
from flask import Flask
from flask.logging import create_logger
import os
from logging.handlers import TimedRotatingFileHandler


class Logging:
    def __init__(self,
                 app: Flask,
                 logs_filename: str | None = None,
                 logs_path: str | None = None,
                 backup_log_files_count: int = 7):

        self.app = app

        self.backup_log_files_count = backup_log_files_count

        self.logs_path = self.__set_logs_path(logs_filename, logs_path)
        self.__logger = create_logger(app)

    def __set_logs_path(self, filename: str, path: str) -> str | None:
        if filename is None or path is None:
            return None

        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        return os.path.join(path, filename)

    def setup(self):
        if self.app.debug:
            self.__logger.setLevel("DEBUG")
        else:
            self.__logger.setLevel("INFO")

        self.__setup_serial()

        if self.logs_path is not None:
            self.__setup_file()

    def __setup_serial(self):
        formatter = self.__get_formatter(with_day=False)

        console_logger = logging.StreamHandler()
        console_logger.setFormatter(formatter)

        self.__logger.addHandler(console_logger)

    def __setup_file(self):
        formatter = self.__get_formatter()

        file_handler = TimedRotatingFileHandler(filename=self.logs_path,
                                                when="midnight",
                                                encoding="utf-8",
                                                backupCount=self.backup_log_files_count)
        file_handler.setFormatter(formatter)

        self.__logger.addHandler(file_handler)

    def __get_formatter(self, with_day: bool = True) -> logging.Formatter:
        format = "%Y-%m-%d %H:%M:%S" if with_day else "%H:%M:%S"

        formatter = logging.Formatter(
            "{asctime} - {name} - {levelname} - {message}",
            style="{",
            datefmt=format,
        )

        return formatter
