from typing import AsyncIterable

from dishka import AnyOf, Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from aiogram_template.config import DatabaseConfig
from aiogram_template.data.database.uow import UoW


class DatabaseProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_engine(self, db_config: DatabaseConfig) -> AsyncIterable[AsyncEngine]:
        engine = create_async_engine(db_config.url)
        yield engine
        await engine.dispose()

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, engine: AsyncEngine
    ) -> AsyncIterable[AnyOf[AsyncSession, UoW]]:
        async with AsyncSession(bind=engine, expire_on_commit=False) as session:
            yield session
