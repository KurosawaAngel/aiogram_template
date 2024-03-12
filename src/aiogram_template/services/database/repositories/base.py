from sqlalchemy.ext.asyncio import AsyncSession

from aiogram_template.services.database.models import Base


class BaseRepository:
    _session: AsyncSession

    __slots__ = ("_session",)

    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    def add(self, *entity: Base) -> None:
        self._session.add_all(entity)
