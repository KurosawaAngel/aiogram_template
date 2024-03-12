from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from .settings import Config


async def on_startup(bot: Bot, config: Config) -> None:
    if config.webhook.use:
        await bot.set_webhook(
            config.webhook_url, drop_pending_updates=config.common.drop_pending_updates
        )
        return
    await bot.delete_webhook(drop_pending_updates=config.common.drop_pending_updates)


async def on_shutdown(bot: Bot, config: Config) -> None:
    if config.webhook.reset:
        await bot.delete_webhook()


def run_webhook(dp: Dispatcher, config: Config, bot: Bot) -> None:
    app = web.Application()
    SimpleRequestHandler(dp, bot, secret_token=config.webhook.secret).register(
        app, path=config.webhook.path
    )
    setup_application(app, dp, bot=bot)
    return web.run_app(app, host=config.webhook.host, port=config.webhook.port)