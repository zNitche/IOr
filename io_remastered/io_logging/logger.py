from typing import Any
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from io_remastered.io_logging.adapters.thread_logger_adapter import ThreadLoggerAdapter


class Logger:
    def __init__(self):
        # set via init() method
        self.debug_mode = False

        self.log_to_file = None
        self.backup_log_files_count = 7
        self.logs_path = None

        self.__logger: logging.Logger | logging.LoggerAdapter[Any] | None = None

    def init(self,
             logger_name: str | None = None,
             debug: bool = False,
             log_to_file: bool = False,
             logs_filename: str | None = None,
             logs_path: str | None = None,
             backup_log_files_count: int = 7):

        self.__logger = Logger.get_logger(logger_name=logger_name)

        self.debug_mode = debug

        self.log_to_file = log_to_file
        self.backup_log_files_count = backup_log_files_count
        self.logs_path = self.__set_logs_path(logs_filename, logs_path)

        self.__setup()

    def __setup(self):
        if self.__logger is None:
            raise Exception("can't setup None logger")

        self.__logger.setLevel(
            "DEBUG" if self.debug_mode else "INFO")
        self.__setup_serial()

        if self.logs_path is not None and self.log_to_file:
            self.__setup_file(logs_path=self.logs_path,
                              backup_log_files_count=self.backup_log_files_count)

    def __setup_serial(self):
        formatter = self.__get_formatter(with_day=False)

        console_logger = logging.StreamHandler()
        console_logger.setFormatter(formatter)

        self.__logger.addHandler(console_logger)  # type: ignore

    def __setup_file(self, logs_path: str, backup_log_files_count: int):
        formatter = self.__get_formatter()

        file_handler = TimedRotatingFileHandler(filename=logs_path,
                                                when="midnight",
                                                encoding="utf-8",
                                                backupCount=backup_log_files_count)
        file_handler.setFormatter(formatter)

        self.__logger.addHandler(file_handler)  # type: ignore

    def __set_logs_path(self, filename: str | None, path: str | None) -> str | None:
        if filename is None or path is None:
            return None

        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        return os.path.join(path, filename)

    def __get_formatter(self, with_day: bool = True) -> logging.Formatter:
        format = "%Y-%m-%d %H:%M:%S" if with_day else "%H:%M:%S"

        formatter = logging.Formatter(
            "{asctime} - {levelname} - {name} - {message}",
            style="{",
            datefmt=format,
        )

        return formatter

    @staticmethod
    def for_thread(logger_name: str, thread_uid: str | int):
        logger = Logger()
        logger.__logger = Logger.get_logger(
            logger_name=logger_name, logger_adapter=ThreadLoggerAdapter, extra_context={"thread_uid": thread_uid})

        return logger

    @staticmethod
    def get_logger(logger_name: str | None,
                   logger_adapter: type[logging.LoggerAdapter] | None = None,
                   extra_context: dict[str, Any] | None = None):

        logger = logging.getLogger(
            __name__ if logger_name is None else logger_name)
        return logger_adapter(logger, extra=extra_context) if logger_adapter else logger

    def exception(self, message: str):
        if not self.__logger:
            raise Exception("logger is None")

        self.__logger.exception(message)

    def error(self, message: str):
        if not self.__logger:
            raise Exception("logger is None")

        self.__logger.error(message)

    def info(self, message: str):
        if not self.__logger:
            raise Exception("logger is None")

        self.__logger.info(message)

    def warning(self, message: str):
        if not self.__logger:
            raise Exception("logger is None")

        self.__logger.warning(message)

    def debug(self, message: str):
        if not self.__logger:
            raise Exception("logger is None")

        self.__logger.debug(message)
