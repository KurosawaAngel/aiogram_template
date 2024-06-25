from datetime import timedelta

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.entities import DIALOG_EVENT_NAME
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from dishka import AsyncContainer
from dishka.integrations.aiogram import ContainerMiddleware

from aiogram_template.config import (
    BotConfig,
    CommonConfig,
    RedisConfig,
    WebhookConfig,
)
from aiogram_template.enums import Locale
from aiogram_template.middlewares.outer import I18nManager
from aiogram_template.utils import mjson


def setup_dispatcher(
    redis_config: RedisConfig,
    config: CommonConfig,
    fluent_core: FluentRuntimeCore,
    container: AsyncContainer,
) -> Dispatcher:
    storage = RedisStorage.from_url(
        url=redis_config.fsm_url,
        json_loads=mjson.decode,
        json_dumps=mjson.encode,
        key_builder=DefaultKeyBuilder(with_destiny=True, with_bot_id=True),
        state_ttl=timedelta(days=35),
        data_ttl=timedelta(days=35),
    )
    dp = Dispatcher(
        storage=storage,
        events_isolation=storage.create_isolation(),
        config=config,
        main_container=container,
    )

    dp.include_routers()
    _setup_middlewares(dp, fluent_core, container)

    dp.startup.register(_on_startup)
    dp.shutdown.register(_on_shutdown)
    return dp


async def _on_startup(
    bot: Bot, main_container: AsyncContainer, dispatcher: Dispatcher
) -> None:
    webhook_config = await main_container.get(WebhookConfig)
    bot_config = await main_container.get(BotConfig)
    if webhook_config.use:
        await bot.set_webhook(
            webhook_config.bot_url,
            drop_pending_updates=bot_config.drop_pending_updates,
            secret_token=webhook_config.secret.get_secret_value(),
            allowed_updates=dispatcher.resolve_used_update_types(
                skip_events={DIALOG_EVENT_NAME}
            ),
        )
    else:
        await bot.delete_webhook(drop_pending_updates=bot_config.drop_pending_updates)


async def _on_shutdown(bot: Bot, main_container: AsyncContainer) -> None:
    webhook_config = await main_container.get(WebhookConfig)
    if webhook_config.reset:
        await bot.delete_webhook()

    await main_container.close()
    await bot.session.close()


def _setup_middlewares(
    dp: Dispatcher, core: FluentRuntimeCore, container: AsyncContainer
) -> None:
    setup_dialogs(dp)
    dp.update.outer_middleware(ContainerMiddleware(container))
    I18nMiddleware(
        core=core,
        manager=I18nManager(),
        default_locale=Locale.DEFAULT,
    ).setup(dp)
