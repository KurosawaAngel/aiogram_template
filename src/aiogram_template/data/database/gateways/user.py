from ..models import DBUser
from .base import BaseGateway


class UserGateway(BaseGateway):
    __slots__ = ()

    async def get_user(self, user_id: int) -> DBUser | None:
        return await self.session.get(DBUser, user_id)
