from aiogram import Dispatcher
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from .runners import shutdown, startup
from .settings import Settings
from .utils import msgspec_json as mjson


def setup_dispatcher(settings: Settings) -> Dispatcher:
    """
    :return: Configured ``Dispatcher`` with installed middlewares and included routers
    """
    storage = RedisStorage.from_url(
        url=settings.redis_host,
        json_loads=mjson.decode,
        json_dumps=mjson.encode,
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )
    dp = Dispatcher(storage=storage)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    return dp
