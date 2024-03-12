from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from .user import UserRepository


class Repository(BaseRepository):
    """Main repository for all sub repositories."""

    __slots__ = ("user",)

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.user = UserRepository(session)
