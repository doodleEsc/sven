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