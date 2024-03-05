from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


def create_pool(dsn: str) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(dsn, pool_size=10, max_overflow=10)
    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_pool
