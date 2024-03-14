from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiogram_template.services.database import Repository

REPOSITORY_NAME = "repository"


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, maker: async_sessionmaker[AsyncSession]) -> None:
        self.maker = maker

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.maker() as session:
            data[REPOSITORY_NAME] = Repository(session)
            return await handler(event, data)
