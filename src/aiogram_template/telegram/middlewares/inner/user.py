from typing import Any, Awaitable, Callable, Dict, cast

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from dishka import AsyncContainer
from dishka.integrations.aiogram import CONTAINER_NAME

from aiogram_template.data.database.gateways import UserGateway


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = cast(User | None, data.get("event_from_user"))
        if user is None or user.is_bot:
            return await handler(event, data)

        container = cast(AsyncContainer, data[CONTAINER_NAME])
        gateway: UserGateway = await container.get(UserGateway)
        db_user = await gateway.upsert_user(user.id, user.username, user.language_code)
        await gateway.commit()
        data["db_user"] = db_user
        return await handler(event, data)
