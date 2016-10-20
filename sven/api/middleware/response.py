from sven.api.wsgi import Response

async def response_factory(app, handler):
    async def response(request):
        resp = await handler(request)
        return resp
    return response
