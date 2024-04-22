from typing import Any, AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from aiogram_template.config import Config
from aiogram_template.services.database import Repository


class DatabaseProvider(Provider):
    scope = Scope.APP

    @provide
    async def create_engine(
        self, config: Config
    ) -> AsyncGenerator[AsyncEngine, Any, None]:
        engine = create_async_engine(config.database_url)
        yield engine
        await engine.dispose()

    @provide
    def create_session_maker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine)

    @provide(Scope=Scope.REQUEST)
    async def get_repository(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncGenerator[Repository, Any, None]:
        async with session_maker() as session:
            yield Repository(session)
