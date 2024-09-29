from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web
from dishka import FromDishka

bot_router = web.RouteTableDef()


@bot_router.post("/bot")
async def handle_bot_update(
    request: web.Request, handler: FromDishka[SimpleRequestHandler]
) -> web.Response:
    return await handler.handle(request)
