from aiohttp import web

routes = web.RouteTableDef()


@routes.post('/submit')
async def submit(request: web.Request) -> web.Response:
    return web.Response(body="ok")


@routes.post('/check')
async def check(request: web.Request):
    return web.Response(body="ok")
