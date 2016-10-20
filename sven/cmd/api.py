import asyncio

from sven.api import wsgi
from aiohttp import web


async def get_func_1(id):
    return web.Response(text=id)

async def get_func_2():
    return web.Response(text="get func without parameters")

async def post_func_1(id):
    return web.Response(text=id)

async def post_func_2():
    return web.Response(text='post func without parameters')

async def delete_func_1(id, name):
    resp = id + name
    return web.Response(text=resp)

async def delete_func_2():
    return web.Response(text='delete func without parameters')

async def put_func_1(id, name):
    resp = id + name
    return web.Response(text=resp)

async def put_func_2():
    return web.Response(text='put func without parameters')


def main():
    loop = asyncio.get_event_loop()
    router = wsgi.Router()
    router.add_route('GET', '/get', wsgi.RequestHandler(get_func_2))
    router.add_route('GET', '/get/{id}', wsgi.RequestHandler(get_func_1))
    router.add_route('POST', '/post', wsgi.RequestHandler(post_func_2))
    router.add_route('POST', '/post/{id}', wsgi.RequestHandler(post_func_1))
    router.add_route('DELETE', '/delete', wsgi.RequestHandler(delete_func_2))
    router.add_route('DELETE', '/delete/{id}', wsgi.RequestHandler(delete_func_1))
    router.add_route('PUT', '/put', wsgi.RequestHandler(put_func_2))
    router.add_route('PUT', '/put/{id}', wsgi.RequestHandler(put_func_1))

    app = wsgi.Application(loop)
    app._router = router
    server = wsgi.Server(app)
    server.run('0.0.0.0', 8000)


if __name__ == '__main__':
    main()
