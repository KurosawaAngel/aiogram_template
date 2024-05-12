from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from aiogram_template.config import PostgresConfig


class DatabaseProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_engine(self, db_config: PostgresConfig) -> AsyncIterable[AsyncEngine]:
        engine = create_async_engine(db_config.url)
        yield engine
        await engine.dispose()

    @provide
    def get_session_maker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session
