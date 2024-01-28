from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from .settings import Settings


async def startup(bot: Bot, settings: Settings):
    if settings.use_webhook:
        return await bot.set_webhook(
            settings.webhook_url, drop_pending_updates=settings.drop_pending_updates
        )
    await bot.delete_webhook(drop_pending_updates=settings.drop_pending_updates)


async def shutdown(bot: Bot, settings: Settings):
    await bot.delete_webhook()


def run_webhook(dp: Dispatcher, settings: Settings, bot: Bot):
    if settings.reset_webhook:
        dp.shutdown.register(shutdown)
    app = web.Application()
    SimpleRequestHandler(dp, bot, secret_token=settings.secret).register(
        app, path=settings.webhook_path
    )
    setup_application(app, dp, bot=bot)
    return web.run_app(app, host=settings.webhook_host, port=settings.webhook_port)
