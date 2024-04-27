from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from dishka.integrations.aiohttp import setup_dishka

from aiogram_template.factories import MAIN_CONTAINER_KEY

from .config import Config


def run_webhook(dp: Dispatcher, config: Config, bot: Bot) -> None:
    app = web.Application()
    setup_dishka(dp[MAIN_CONTAINER_KEY], app)
    SimpleRequestHandler(
        dp, bot, secret_token=config.webhook.secret.get_secret_value()
    ).register(app, path=config.webhook.path)

    setup_application(app, dp, bot=bot)
    return web.run_app(app, host=config.webhook.host, port=config.webhook.port)
