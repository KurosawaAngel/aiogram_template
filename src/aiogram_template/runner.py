import asyncio
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram_dialog.api.entities import DIALOG_EVENT_NAME
from aiohttp import web
from dishka import AsyncContainer, FromDishka
from dishka.integrations.aiohttp import setup_dishka

from aiogram_template import handlers
from aiogram_template.config import WebhookConfig


def run_webhook(config: WebhookConfig, container: AsyncContainer) -> None:
    app = web.Application()
    app.add_routes((handlers.bot_router,))
    app.on_startup.append(_on_startup)
    app.on_shutdown.append(_on_shutdown)
    setup_dishka(container, app, auto_inject=True)

    return web.run_app(app, host=config.host, port=config.port)


def run_polling(container: AsyncContainer) -> None:
    with suppress(KeyboardInterrupt):
        asyncio.run(start_polling(container))


async def start_polling(container: AsyncContainer) -> None:
    dp = await container.get(Dispatcher)
    bot = await container.get(Bot)
    try:
        await dp.start_polling(
            bot,
            polling_timeout=60,
            allowed_updates=dp.resolve_used_update_types(
                skip_events={DIALOG_EVENT_NAME}
            ),
        )
    finally:
        await container.close()


async def _on_startup(
    app: web.Application, dp: FromDishka[Dispatcher], bot: FromDishka[Bot]
) -> None:
    workflow_data = {
        "app": app,
        "dispatcher": dp,
        "bot": bot,
        **dp.workflow_data,
    }
    await dp.emit_startup(**workflow_data)


async def _on_shutdown(
    app: web.Application, dp: FromDishka[Dispatcher], bot: FromDishka[Bot]
) -> None:
    workflow_data = {
        "app": app,
        "dispatcher": dp,
        "bot": bot,
        **dp.workflow_data,
    }
    await dp.emit_shutdown(**workflow_data)
