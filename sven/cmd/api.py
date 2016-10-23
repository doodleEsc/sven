from sven.api.wsgi import Server, Application
from sven.api.middleware import auth_factory

middlewares = [auth_factory]
app = Application(middlewares=middlewares)


@app.get('/get')
async def get_func_2():
    return {
        "template": "index.html",
        "name": "cookie"
    }


if __name__ == '__main__':
    server = Server(app)
    server.run('0.0.0.0', 8000)
