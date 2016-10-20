import inspect
import functools

from urllib import parse
from json.decoder import JSONDecodeError

from aiohttp import web


def has_request(func):
    parameters = inspect.signature(func).parameters
    return True if "request" in parameters.keys() else False


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
    def __init__(self, loop=None):
        super().__init__(loop=loop)

    def get(self, path):
        """
        define app.get('/path')
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            self.router.add_route('GET', path, RequestHandler(wrapper))
            return wrapper
        return decorator

    def post(self, path):
        """
        define app.post('/path')
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            self.router.add_route('POST', path, RequestHandler(wrapper))
            return wrapper
        return decorator

    def put(self, path):
        """
        define app.post('/path')
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            self.router.add_route('PUT', path, RequestHandler(wrapper))
            return wrapper
        return decorator

    def delete(self, path):
        """
        define app.post('/path')
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            self.router.add_route('DELETE', path, RequestHandler(wrapper))
            return wrapper
        return decorator

    def copy(self):
        raise NotImplemented


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
                return Response(text="INVALID JSON OBJECT")
            kw.update(params)
        except JSONDecodeError:
            if request.method == 'POST' or request.method == 'PUT':
                return Response(text='NO JSON OBJECT FOUND')

        # get 'request' parameters
        if self.has_request:
            kw['request'] = request

        return await self._func(**kw)


class Response(web.Response):

    def __init__(self, status=200, headers=None,
                 content_type=None, charset=None,
                 body=None, text=None):
        super().__init__(status=status, headers=headers,
                         content_type=content_type, charset=charset,
                         body=body, text=text)
