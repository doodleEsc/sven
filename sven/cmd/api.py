import asyncio

from sven.api.wsgi import Application, Server
from sven.api.wsgi import init_template_engine
from sven.db.utils import create_pool



# async def init(loop):
#     handlers = [
#         'sven.api.handler.index'
#     ]
#     middlewares = [
#         'sven.api.middleware.auth_factory'
#     ]
#     template_engine = init_template_engine('E:/Python_Project/sven/sven/templates')
#
#     await create_pool(loop, host='10.133.145.254', port=3306,
#                       user='test', password='test', db='sven')
#
#     app = Application(loop=loop,
#                       handlers=handlers,
#                       middlewares=middlewares,
#                       template_engine=template_engine)
#     # server = Server(app)
#     # server.run('0.0.0.0', 8000)
#     handler = app.make_handler()
#     server = await loop.create_server(handler, '0.0.0.0', 8000)
#     return server, app, handler
#
#
# def main():
#     loop = asyncio.get_event_loop()
#     server, app, handler = loop.run_until_complete(init(loop))
#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         pass
#     finally:
#         server.close()
#         loop.run_until_complete(server.wait_closed())
#         loop.run_until_complete(app.shutdown())
#         loop.run_until_complete(handler.shutdown(shutdown_timeout))
#         loop.run_until_complete(app.cleanup())
#     loop.close()


# def run_app(app, *, host='0.0.0.0', port=None,
#             shutdown_timeout=60.0, ssl_context=None,
#             print=print, backlog=128, access_log_format=None,
#             access_log=None):
#     """Run an app locally"""
#     if port is None:
#         if not ssl_context:
#             port = 8080
#         else:
#             port = 8443
#
#     loop = app.loop
#
#     make_handler_kwargs = dict()
#     if access_log_format is not None:
#         make_handler_kwargs['access_log_format'] = access_log_format
#     handler = app.make_handler(access_log=access_log,
#                                **make_handler_kwargs)
#
#     loop.run_until_complete(app.startup())
#     srv = loop.run_until_complete(loop.create_server(handler, host,
#                                                      port, ssl=ssl_context,
#                                                      backlog=backlog))
#
#     scheme = 'https' if ssl_context else 'http'
#     url = URL('{}://localhost'.format(scheme))
#     url = url.with_host(host).with_port(port)
#     print("======== Running on {} ========\n"
#           "(Press CTRL+C to quit)".format(url))
#
#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:  # pragma: no cover
#         pass
#     finally:
#         srv.close()
#         loop.run_until_complete(srv.wait_closed())
#         loop.run_until_complete(app.shutdown())
#         loop.run_until_complete(handler.shutdown(shutdown_timeout))
#         loop.run_until_complete(app.cleanup())
#     loop.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_pool(loop, host='10.133.145.254',
                                        user='test', password='test', db='sven'))
    handlers = [
        'sven.api.handler.index'
    ]
    middlewares = [
        'sven.api.middleware.auth_factory'
    ]
    template_engine = init_template_engine('E:/Python_Project/sven/sven/templates')

    app = Application(loop=loop,
                      handlers=handlers,
                      middlewares=middlewares,
                      template_engine=template_engine)
    server = Server(app)
    server.run(host='0.0.0.0', port=8000)


