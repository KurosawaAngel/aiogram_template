from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


def create_session_maker(dsn: str) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(dsn)
    session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_maker
