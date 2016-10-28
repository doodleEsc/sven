"""
log module
"""

import os
import logging

from sven.utils.singletone import singleton


@singleton
class Log(object):

    def __init__(self):
        pass

    def _init_env(self):
        NORMAL_FILE = 'E:/log/access.log'
        ERROR_FILE = 'E:/log/error.log'
        try:
            path_exist = os.path.exists('E:/log')
            if not path_exist:
                os.mkdir('E:/log')
        except OSError:
            pass