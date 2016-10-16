import os
import asyncio

from aiohttp import web
from aiohttp import web_urldispatcher


class Server(object):
    """Server class that handle service

    manage service
    """

    def __init__(self, app):
        self._app = app

    def run(self, host, port):
        web.run_app(self, host=host, port=port)

class Application(web.Application):
    """wsgi application

    wsgi application class.
    """
    def __init__(self, loop):
        super().__init__(loop=loop)

class Router(web_urldispatcher.UrlDispatcher):
    """router class that handle route info
    read from config file to load handler
    """
    def __init__(self):
        pass


class RequestHandler(object):
    """get params from request
    """

    def __init__(self):
        pass