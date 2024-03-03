from aiogram import Dispatcher
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from .runners import on_shutdown, on_startup
from .settings import Settings
from .utils import msgspec_json as mjson


def setup_dispatcher(settings: Settings) -> Dispatcher:
    """
    :return: Configured ``Dispatcher`` with installed middlewares and included routers
    """
    storage = RedisStorage.from_url(
        url=settings.redis_url,
        json_loads=mjson.decode,
        json_dumps=mjson.encode,
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )
    dp = Dispatcher(
        storage=storage,
        events_isolation=storage.create_isolation(),
        settiongs=settings,
    )
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    return dp
