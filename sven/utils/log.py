"""
log module
"""

import os
import logging
import logging.handlers

from sven.utils.singletone import singleton
from sven.api.exception.path import PathNotFoundError

NORMAL_FILE = 'E:/log/access.log'
ERROR_FILE = 'E:/log/error.log'
LOG_PATH = 'E:/log'


@singleton
class Log(object):

    def __init__(self):
        self._init_env()

    def _init_env(self):
        try:
            path_exist = os.path.exists(LOG_PATH)
            if not path_exist:
                os.mkdir(LOG_PATH)
        except OSError:
            raise PathNotFoundError("Paht %s Not Found" %LOG_PATH)

        error_handler = logging.handlers.RotatingFileHandler(ERROR_FILE, maxBytes=1024*1024, backupCount=3)
        error_handler.setLevel(logging.ERROR)

        normal_handler = logging.handlers.RotatingFileHandler(NORMAL_FILE, maxBytes=1024*1024, backupCount=3)
        normal_handler.setLevel(logging.DEBUG)

        fmt_str = '%(asctime)s %(filename)s:%(lineno)s %(levelname)-8s [-] %(message)s'
        fmt = logging.Formatter(fmt_str)

        normal_filter = NormalFilter()
        error_filter = ErrorFilter()

        error_handler.setFormatter(fmt)
        normal_handler.setFormatter(fmt)

        error_handler.addFilter(error_filter)
        normal_handler.addFilter(normal_filter)

        self.logger = logging.getLogger('sven')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(normal_handler)
        self.logger.addHandler(error_handler)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def debug(self, msg):
        self.logger.debug(msg)


class NormalFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.DEBUG, logging.INFO, logging.WARNING)


class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.ERROR, logging.CRITICAL)
