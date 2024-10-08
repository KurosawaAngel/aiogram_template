from datetime import timedelta

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.entities import DIALOG_EVENT_NAME
from aiogram_dialog.widgets.text.jinja import JINJA_ENV_FIELD
from aiogram_i18n.cores import BaseCore
from dishka import AsyncContainer, FromDishka, Provider, Scope, provide
from dishka.integrations.aiogram import (
    CONTAINER_NAME,
    inject,
    setup_dishka,
)
from jinja2 import Environment
from redis.asyncio import Redis

from aiogram_template.config import (
    BotConfig,
    CommonConfig,
    WebhookConfig,
)
from aiogram_template.telegram import handlers
from aiogram_template.telegram.middlewares.inner.user import UserMiddleware


class DispatcherProvider(Provider):
    scope = Scope.APP

    @provide
    def get_webhook_handler(
        self, dp: Dispatcher, bot: Bot, config: WebhookConfig
    ) -> SimpleRequestHandler:
        return SimpleRequestHandler(dp, bot, secret_token=config.secret)

    @provide
    def get_dispatcher(
        self,
        redis: Redis,
        config: CommonConfig,
        container: AsyncContainer,
        i18n_core: BaseCore,
        jinja_env: Environment,
    ) -> Dispatcher:
        storage = RedisStorage(
            redis,
            key_builder=DefaultKeyBuilder(
                with_destiny=True, with_bot_id=True, with_business_connection_id=True
            ),
            state_ttl=timedelta(days=35),
            data_ttl=timedelta(days=35),
        )
        dp = Dispatcher(
            storage=storage,
            events_isolation=storage.create_isolation(),
            config=config,
        )
        dp[CONTAINER_NAME] = container
        dp[JINJA_ENV_FIELD] = jinja_env

        dp.include_routers(handlers.admin_router)
        _setup_middlewares(dp, container, i18n_core)

        dp.startup.register(_on_startup)
        return dp


@inject
async def _on_startup(
    bot: Bot,
    dispatcher: Dispatcher,
    webhook_config: FromDishka[WebhookConfig],
    bot_config: FromDishka[BotConfig],
) -> None:
    if webhook_config.use:
        await bot.set_webhook(
            webhook_config.bot_url,
            drop_pending_updates=bot_config.drop_pending_updates,
            secret_token=webhook_config.secret,
            allowed_updates=dispatcher.resolve_used_update_types(
                skip_events={DIALOG_EVENT_NAME}
            ),
        )
    else:
        await bot.delete_webhook(drop_pending_updates=bot_config.drop_pending_updates)


def _setup_middlewares(
    dp: Dispatcher, container: AsyncContainer, i18n_core: BaseCore
) -> None:
    setup_dialogs(dp, events_isolation=dp.fsm.events_isolation)
    setup_dishka(container, dp, auto_inject=True)
    dp.message.middleware(UserMiddleware())
    dp.callback_query.middleware(UserMiddleware())
