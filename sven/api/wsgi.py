import inspect
from urllib import parse
from json.decoder import JSONDecodeError

from aiohttp import web
from jinja2 import Environment, FileSystemLoader

from sven.api.response import Response
from sven.utils import importutil
from sven.utils.log import Log

logger = Log()

RESPONSE_FACTORY = 'sven.api.response.response_factory'


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
    logger.info('add template %s' % templates_path)
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
        logger.info('server start at %s:%s' % (host, port))
        web.run_app(self._app, host=host, port=port)


class Application(web.Application):
    """wsgi application

    wsgi application class.
    """

    def __init__(self, loop=None, handlers=None, middlewares=None, template_engine=None):
        #self.template_engine = init_template_engine(config.template_path)
        self.template_engine = template_engine

        if not isinstance(middlewares, list) or middlewares is None:
            middlewares = []
        middlewares.append(RESPONSE_FACTORY)
        middlewares = tuple(map(importutil.import_function, middlewares))

        super().__init__(loop=loop, middlewares=middlewares)

        self.add_handlers(handlers)

    def copy(self):
        raise NotImplemented

    def render_template(self, template, body):
        if isinstance(self.template_engine, Environment):
            return self.template_engine.get_template(template).render(**body)
        else:
            raise NotImplemented

    def add_handlers(self, modules):
        if not isinstance(modules, list):
            # Here should raise an exception
            raise FileNotFoundError()
        if len(modules) == 0:
            raise ImportError("no handlers")
        for module_str in modules:
            module = importutil.import_module(module_str)
            # get wsgi handler function
            for attr in dir(module):
                if attr.startswith('_'):
                    continue
                func = getattr(module, attr)
                if callable(func):
                    method = getattr(func, '__method__', None)
                    route = getattr(func, '__route__', None)
                    if method and route:
                        self.router.add_route(method, route, RequestHandler(func))


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
