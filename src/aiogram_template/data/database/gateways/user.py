from sqlalchemy.dialects.postgresql import insert

from ..models import DBUser
from .base import BaseGateway


class UserGateway(BaseGateway):
    __slots__ = ()

    async def get_user_by_id(self, user_id: int) -> DBUser | None:
        return await self.session.get(DBUser, user_id)

    async def upsert_user(
        self, tg_id: int, username: str | None, locale: str | None
    ) -> DBUser | None:
        return await self.session.scalar(
            insert(DBUser)
            .values(tg_id=tg_id, username=username, locale=locale)
            .on_conflict_do_update(
                index_elements=["tg_id"], set_={"username": username}
            )
            .returning(DBUser)
        )
