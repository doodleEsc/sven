import inspect
import functools
from urllib import parse
from json.decoder import JSONDecodeError

from aiohttp import web
from jinja2 import Environment, FileSystemLoader

# test code for config

config = dict(
    templates_path='E:/Python_Project/templates'
)


def has_request(func):
    parameters = inspect.signature(func).parameters
    return True if "request" in parameters.keys() else False


def init_template_engine(templates_path, filters=None,
                         autoescape=True, block_start_string='{%',
                         block_end_string='%}', variable_start_string='{{',
                         variable_end_string='}}', auto_reload=True):
    options = dict(
        autoescape=autoescape,
        block_start_string=block_start_string,
        block_end_string=block_end_string,
        variable_start_string=variable_start_string,
        variable_end_string=variable_end_string,
        auto_reload=auto_reload
    )
    env = Environment(loader=FileSystemLoader(templates_path), **options)
    if filters is not None and isinstance(filters, dict):
        for name, func in filters.items():
            env.filters[name] = func

    return env


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

    def __init__(self, loop=None, middlewares=None):
        self.template_engine = init_template_engine(config['templates_path'])
        if not isinstance(middlewares, list) or middlewares is None:
            middlewares = []
        middlewares.append(response_factory)
        super().__init__(loop=loop, middlewares=middlewares)

    def get(self, path):
        """
        define app.get('/path')
        :param path: restful url
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
        :param path: restful url
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
        :param path: restful url
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
        :param path: restful url
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

async def response_factory(app, handler):
    async def response(request):
        resp = await handler(request)
        return resp
    return response
