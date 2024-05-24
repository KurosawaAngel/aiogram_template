from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram_dialog.api.entities import DIALOG_EVENT_NAME
from aiohttp import web
from dishka import AsyncContainer, FromDishka
from dishka.integrations import aiohttp

from aiogram_template.config import WebhookConfig


@aiohttp.inject
async def _setup_webhook(
    app: web.Application,
    dispatcher: FromDishka[Dispatcher],
    bot: FromDishka[Bot],
    config: FromDishka[WebhookConfig],
) -> None:
    SimpleRequestHandler(
        dispatcher, bot, secret_token=config.secret.get_secret_value()
    ).register(app, path=config.path)

    setup_application(app, dispatcher)


def run_webhook(config: WebhookConfig, container: AsyncContainer) -> None:
    app = web.Application()
    aiohttp.setup_dishka(container, app)
    app.on_startup.append(_setup_webhook)

    return web.run_app(app, host=config.host, port=config.port)


async def run_polling(container: AsyncContainer) -> None:
    dispatcher = await container.get(Dispatcher)
    bot = await container.get(Bot)
    await dispatcher.start_polling(
        bot,
        allowed_updates=dispatcher.resolve_used_update_types(
            skip_events={DIALOG_EVENT_NAME}
        ),
    )
