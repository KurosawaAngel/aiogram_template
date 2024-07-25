import logging

from dishka import make_async_container

from aiogram_template.config import Config
from aiogram_template.di import (
    BotProvider,
    ConfigProvider,
    DatabaseProvider,
    DispatcherProvider,
    GatewayProvider,
    JinjaProvider,
)
from aiogram_template.runner import run_polling, run_webhook


def main() -> None:
    config = Config.create()
    main_container = make_async_container(
        ConfigProvider(),
        DatabaseProvider(),
        GatewayProvider(),
        BotProvider(),
        DispatcherProvider(),
        JinjaProvider(),
        context={
            Config: config,
        },
    )

    if config.webhook.use:
        return run_webhook(config.webhook, main_container)

    run_polling(main_container)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(name)s - %(asctime)s | %(levelname)s | %(message)s",
        level=logging.INFO,
        datefmt="%d/%m/%Y %H:%M:%S",
    )
    main()
