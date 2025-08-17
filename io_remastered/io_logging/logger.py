from typing import Any
import os
import logging
from io_remastered.io_logging import common
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
        self.logs_path = common.set_logs_path(
            filename=logs_filename, path=logs_path)

        self.__setup()

    def __setup(self):
        if self.__logger is None:
            raise Exception("can't setup None logger")

        common.setup(logger=self.__logger, logs_path=self.logs_path,
                     is_debug=self.debug_mode, backup_log_files_count=self.backup_log_files_count)

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
