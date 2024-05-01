from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram_dialog.api.entities import DIALOG_EVENT_NAME
from aiohttp import web
from dishka import AsyncContainer, FromDishka
from dishka.integrations import aiogram, aiohttp

from aiogram_template.config import Config
from aiogram_template.di import MAIN_CONTAINER_KEY


@aiohttp.inject
async def _setup_webhook(
    app: web.Application,
    dispatcher: FromDishka[Dispatcher],
    bot: FromDishka[Bot],
    config: FromDishka[Config],
) -> None:
    container: AsyncContainer = app[aiohttp.DISHKA_CONTAINER_KEY]
    dispatcher[MAIN_CONTAINER_KEY] = container
    aiogram.setup_dishka(container, dispatcher)

    SimpleRequestHandler(
        dispatcher, bot, secret_token=config.webhook.secret.get_secret_value()
    ).register(app, path=config.webhook.path)

    setup_application(app, dispatcher)


def run_webhook(config: Config, container: AsyncContainer) -> None:
    app = web.Application()
    aiohttp.setup_dishka(container, app)
    app.on_startup.append(_setup_webhook)

    return web.run_app(app, host=config.webhook.host, port=config.webhook.port)


async def run_polling(container: AsyncContainer) -> None:
    bot = await container.get(Bot)
    dispatcher = await container.get(Dispatcher)
    dispatcher[MAIN_CONTAINER_KEY] = container
    aiogram.setup_dishka(container, dispatcher)

    await dispatcher.start_polling(
        bot,
        allowed_updates=dispatcher.resolve_used_update_types(
            skip_events={DIALOG_EVENT_NAME}
        ),
    )
