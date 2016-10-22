from sven.api import wsgi
from sven.api.wsgi import Response
from sven.api.middleware import auth_factory

middlewares = [auth_factory]
app = wsgi.Application(middlewares=middlewares)


@app.get('/get/{id}')
async def get_func_1(id):
    return Response(text=id)


@app.get('/get')
async def get_func_2():
    return Response(text="get func without parameters")


@app.post('/post/{id}')
async def post_func_1(id, name):
    resp = id + name
    return Response(text=resp)


@app.post('/post')
async def post_func_2():
    return Response(text='post func without parameters')


@app.delete('/delete/{id}')
async def delete_func_1(id):
    resp = id
    return Response(text=resp)


@app.delete('/delete')
async def delete_func_2():
    return Response(text='delete func without parameters')


@app.put('/put/{id}')
async def put_func_1(id, name):
    resp = id + name
    return Response(text=resp)


@app.put('/put')
async def put_func_2():
    return Response(text='put func without parameters')


if __name__ == '__main__':
    server = wsgi.Server(app)
    server.run('0.0.0.0', 8000)
