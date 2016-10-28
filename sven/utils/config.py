"""
parse configuration
"""
from configparser import ConfigParser
from sven.utils import importutil
from sven.utils.singletone import singleton


@singleton
class Config(object):
    """
    config module
    """
    def __init__(self, path):
        self.path = path
        self.cp = ConfigParser()
        self.cp.read(self.path)
        self.database = dict()
        self.middlewares = list()
        self.handlers = None
        self.template_path = None
        self.static_path = None
        self.init_config()

    def init_config(self):
        self._get_database()
        self._get_middlewares()
        self._get_handlers()
        self._get_template_path()
        self._get_static_path()

    def _get_database(self):
        items = self.cp.items('database')
        for k, v in items:
            self.database[k] = v

    def _get_middlewares(self):
        ms = self.cp.get('middlewares', 'middlewares')
        middlewares = ms.split(',')
        if len(middlewares) == 1 and middlewares[0] == '':
            middlewares = []
        for middleware in middlewares:
            func = importutil.import_function(middleware)
            self.middlewares.append(func)

    def _get_handlers(self):
        hs = self.cp.get('handlers', 'handlers')
        handlers = hs.split(',')
        if len(handlers) == 1 and handlers[0] == '':
            handlers = []
        self.handlers = handlers

    def _get_template_path(self):
        template_path = self.cp.get('template', 'template_path')
        self.template_path = template_path

    def _get_static_path(self):
        static_path = self.cp.get('static', 'static_path')
        self.static_path = static_path



