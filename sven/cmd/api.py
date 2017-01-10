import asyncio

from sven.utils.log import Log
from sven.api.wsgi import Application, Server
from sven.api.wsgi import init_template_engine
from sven.db.utils import create_pool


if __name__ == '__main__':
    logger = Log(log_path='F:/log/')

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
    static_path = 'E:/Python_Project/sven/sven/static'
    app = Application(loop=loop,
                      handlers=handlers,
                      static_path=static_path,
                      middlewares=middlewares,
                      template_engine=template_engine)
    server = Server(app)
    logger.info("begin to start server")
    server.run(host='0.0.0.0', port=8000)


