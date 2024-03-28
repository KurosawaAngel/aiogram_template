from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncEngine

from .configs import Config


async def on_startup(bot: Bot, config: Config, dispatcher: Dispatcher) -> None:
    if config.webhook.use:
        await bot.set_webhook(
            config.webhook_url,
            drop_pending_updates=config.common.drop_pending_updates,
            secret_token=config.webhook.secret.get_secret_value(),
            allowed_updates=dispatcher.resolve_used_update_types(),
        )
        return
    await bot.delete_webhook(drop_pending_updates=config.common.drop_pending_updates)


async def on_shutdown(bot: Bot, config: Config, engine: AsyncEngine) -> None:
    if config.webhook.reset:
        await bot.delete_webhook()
    await engine.dispose()


def run_webhook(dp: Dispatcher, config: Config, bot: Bot) -> None:
    app = web.Application()
    SimpleRequestHandler(
        dp, bot, secret_token=config.webhook.secret.get_secret_value()
    ).register(app, path=config.webhook.path)

    setup_application(app, dp, bot=bot)
    return web.run_app(app, host=config.webhook.host, port=config.webhook.port)
