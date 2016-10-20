import os
import inspect
import asyncio

from urllib import parse
from json.decoder import JSONDecodeError

from aiohttp import web
from aiohttp import web_urldispatcher


class Server(object):
    """Server class that handle service
    manage service
    """
    def __init__(self, app):
        self._app = app

    def run(self, host, port):
        web.run_app(self._app, host=host, port=port)


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
    # def __init__(self):
    #     pass

    def add_routes(self):
        pass


# def has_params(func):
#     parameters = inspect.signature(func).parameters
#     return True if len(parameters.items()) > 0 else False


def has_request(func):
    parameters = inspect.signature(func).parameters
    return True if "request" in parameters.keys() else False


class RequestHandler(object):
    """get params from request
    """

    def __init__(self, func):
        self._func = func
        self.has_request = has_request(func)

    async def __call__(self, request):
        # get resource id parameter
        kw = dict(**request.match_info)

        # get query string parameters
        query_string = request.query_string
        if query_string:
            for k, v in parse.parse_qs(query_string).items():
                kw[k] = v[0]

        # get json parameters
        try:
            params = await request.json()
            if not isinstance(params, dict):
                return web.HTTPBadRequest(text="INVALID JSON OBJECT")
            kw.update(params)
        except JSONDecodeError:
            if request.method == 'POST' or request.method == 'PUT':
                return web.HTTPBadRequest(text='NO JSON OBJECT FOUND')

        # get 'request' parameters
        if self.has_request:
            kw['request'] = request

        return await self._func(**kw)
