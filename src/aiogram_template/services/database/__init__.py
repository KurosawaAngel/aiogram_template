from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .models import DBUser
from .repositories import Repository

__all__ = ["create_engine", "create_maker", "DBUser", "Repository"]


def create_engine(dsn: str) -> AsyncEngine:
    return create_async_engine(dsn)


def create_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)
