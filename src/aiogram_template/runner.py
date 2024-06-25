from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram_dialog.api.entities import DIALOG_EVENT_NAME
from aiohttp import web
from dishka import AsyncContainer
from dishka.integrations import aiohttp

from aiogram_template.config import WebhookConfig


def _setup_webhook(
    app: web.Application,
    bot: Bot,
    dispatcher: Dispatcher,
    config: WebhookConfig,
) -> None:
    SimpleRequestHandler(
        dispatcher, bot, secret_token=config.secret.get_secret_value()
    ).register(app, path=config.path)

    setup_application(app, dispatcher, bot=bot)


def run_webhook(
    config: WebhookConfig, container: AsyncContainer, bot: Bot, dispatcher: Dispatcher
) -> None:
    app = web.Application()
    aiohttp.setup_dishka(container, app)
    _setup_webhook(app, bot, dispatcher, config)

    return web.run_app(app, host=config.host, port=config.port)


def run_polling(bot: Bot, dispatcher: Dispatcher) -> None:
    dispatcher.run_polling(
        bot,
        allowed_updates=dispatcher.resolve_used_update_types(
            skip_events={DIALOG_EVENT_NAME}
        ),
        polling_timeout=60,
    )
