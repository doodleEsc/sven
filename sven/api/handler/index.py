from sven.api.decorator import get


@get('/')
async def index():
    return {
        "template": "index.html",
        "name": "cookie"
    }


