import asyncio

from sven.api import wsgi


def main():
    loop = asyncio.get_event_loop()
    router = wsgi.Router()
    app = wsgi.Application(loop)
    server = wsgi.Server(app)
    server.run('0.0.0.0', 8000)