from aiogram import Dispatcher
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram_dialog import setup_dialogs

from aiogram_template.middlewares.outer import DBSessionMiddleware
from aiogram_template.runners import on_shutdown, on_startup
from aiogram_template.services.database import create_session_maker
from aiogram_template.settings import Config
from aiogram_template.utils import msgspec_json as mjson


def _setup_middlewares(dp: Dispatcher, config: Config) -> None:
    """
    Setup middlewares for dispatcher

    :param dp: Dispatcher instance
    :param config: Application config

    :return: None
    """
    session_maker = create_session_maker(config.postgres_url)
    dp.update.outer_middleware(DBSessionMiddleware(session_maker))


def setup_dispatcher(config: Config) -> Dispatcher:
    """
    Setup dispatcher with installed middlewares and included routers

    :param config: Application config

    :return: Configured ``Dispatcher`` with installed middlewares and included routers
    """
    storage = RedisStorage.from_url(
        url=config.redis_url,
        json_loads=mjson.decode,
        json_dumps=mjson.encode,
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )
    dp = Dispatcher(
        storage=storage,
        events_isolation=storage.create_isolation(),
        config=config,
    )
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    setup_dialogs(dp)
    return dp
