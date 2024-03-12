from ..models import DBUser
from .base import BaseRepository


class UserRepository(BaseRepository):
    __slots__ = ()

    async def get(self, user_id: int) -> DBUser | None:
        return await self._session.get(DBUser, user_id)
