from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)


def create_engine(dsn: str) -> AsyncEngine:
    """Create a new async engine."""
    return create_async_engine(dsn)


def create_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create a new session maker."""
    return async_sessionmaker(bind=engine, expire_on_commit=False)
