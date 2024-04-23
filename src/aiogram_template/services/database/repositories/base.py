from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    _session: AsyncSession

    __slots__ = ("_session",)

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()
