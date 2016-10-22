"""
auth middleware
"""

async def auth_factory(app, handler):
    async def check_auth(request):
        # code here to check auth
        print("auth check")
        return await handler(request)
    return check_auth
