from sven.api.decorator import get
from sven.api.response import HTTPBadRequest


@get('/')
async def index():
    return {
        "template": "index.html",
        "name": "cookie"
    }


@get('/bad')
async def bad():
    return HTTPBadRequest(text='bad request')
