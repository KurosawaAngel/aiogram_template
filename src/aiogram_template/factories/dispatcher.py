from aiogram import Dispatcher
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from aiogram_template.runners import on_shutdown, on_startup
from aiogram_template.settings import Config
from aiogram_template.utils import msgspec_json as mjson


def setup_dispatcher(config: Config) -> Dispatcher:
    """
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
    return dp
