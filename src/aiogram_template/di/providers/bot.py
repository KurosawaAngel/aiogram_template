from typing import AsyncIterable

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from dishka import Provider, Scope, provide

from aiogram_template.config import BotConfig
from aiogram_template.middlewares.request import RetryRequestMiddleware
from aiogram_template.utils import mjson


class BotProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_bot(self, bot_config: BotConfig) -> AsyncIterable[Bot]:
        session = AiohttpSession(json_loads=mjson.decode, json_dumps=mjson.encode)
        session.middleware(RetryRequestMiddleware())
        async with Bot(
            token=bot_config.token.get_secret_value(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
            session=session,
        ).context() as bot:
            yield bot