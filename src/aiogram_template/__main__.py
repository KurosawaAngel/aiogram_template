import logging

from aiogram import Bot
from aiogram_i18n.cores import FluentRuntimeCore
from dishka import make_async_container

from aiogram_template.config import Config
from aiogram_template.di import (
    ConfigProvider,
    ContextProvider,
    DatabaseProvider,
    GatewayProvider,
)
from aiogram_template.factory import setup_bot, setup_dispatcher, setup_fluent_core
from aiogram_template.runner import run_polling, run_webhook


def main() -> None:
    config = Config.create()
    bot = setup_bot(config.bot)
    fluent = setup_fluent_core()
    main_container = make_async_container(
        ConfigProvider(),
        DatabaseProvider(),
        GatewayProvider(),
        ContextProvider(),
        context={
            Config: config,
            Bot: bot,
            FluentRuntimeCore: fluent,
        },
    )
    dp = setup_dispatcher(
        config.redis,
        config.common,
        fluent,
        main_container,
    )
    if config.webhook.use:
        return run_webhook(config.webhook, main_container, bot, dp)

    run_polling(bot, dp)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(name)s - %(asctime)s | %(levelname)s | %(message)s",
        level=logging.INFO,
        datefmt="%d/%m/%Y %H:%M:%S",
    )
    main()
