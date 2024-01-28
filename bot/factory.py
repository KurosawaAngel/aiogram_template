from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from .runners import startup
from .settings import Settings


def setup_dispatcher(settings: Settings) -> Dispatcher:
    if settings.use_redis:
        redis = Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_database,
        )
        storage = RedisStorage(redis)
    else:
        storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.startup.register(startup)
    return dp
