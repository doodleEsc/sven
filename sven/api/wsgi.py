import os
import inspect
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

    def add_routes(self):
        pass


class RequestHandler(object):
    """get params from request
    """

    def __init__(self, func):
        self._func = func
        self.has_params = self.has_params(func)

    def has_params(self, func):
        parameters = inspect.signature(func).parameters
        return True if len(parameters.items()) > 0 else False

    async def __call__(self, request):
        kw = None
        if self.has_params:
            pass
        else:
            pass

        return await self._func(**kw)
