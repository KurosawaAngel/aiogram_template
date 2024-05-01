import asyncio
import logging

from dishka import make_async_container

from aiogram_template.config import Config
from aiogram_template.di.providers import (
    BotProvider,
    ContextProvider,
    DatabaseProvider,
    DispatcherProvider,
)
from aiogram_template.runner import run_polling, run_webhook


def main() -> None:
    config = Config.create()
    main_container = make_async_container(
        ContextProvider(),
        DatabaseProvider(),
        DispatcherProvider(),
        BotProvider(),
        context={Config: config},
    )
    if config.webhook.use:
        return run_webhook(config, main_container)

    asyncio.run(run_polling(main_container))


if __name__ == "__main__":
    logging.basicConfig(
        format="%(name)s - %(asctime)s | %(levelname)s | %(message)s",
        level=logging.INFO,
        datefmt="%d/%m/%Y %H:%M:%S",
    )
    main()
