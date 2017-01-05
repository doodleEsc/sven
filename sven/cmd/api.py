import asyncio

from sven.api.wsgi import Server, Application
from sven.api.wsgi import init_template_engine


def main():
    loop = asyncio.get_event_loop()
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
    server.run('0.0.0.0', 8000)


if __name__ == '__main__':
    main()
