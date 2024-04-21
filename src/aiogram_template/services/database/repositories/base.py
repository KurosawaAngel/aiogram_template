from sqlalchemy.ext.asyncio import AsyncSession

from aiogram_template.services.database.models import BaseModel


class BaseRepository:
    _session: AsyncSession

    __slots__ = ("_session",)

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    def add(self, *entity: BaseModel) -> None:
        self._session.add_all(entity)
