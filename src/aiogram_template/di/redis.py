from typing import AsyncIterable

from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from aiogram_template.config import RedisConfig


class RedisProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_redis(self, config: RedisConfig) -> AsyncIterable[Redis]:
        redis = Redis.from_url(config.url)
        yield redis
        await redis.close()
