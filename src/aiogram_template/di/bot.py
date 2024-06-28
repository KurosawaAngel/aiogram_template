from typing import AsyncIterable

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from dishka import Provider, Scope, provide

from aiogram_template.config import BotConfig
from aiogram_template.middlewares.request import RetryRequestMiddleware


class BotProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_bot(config: BotConfig) -> AsyncIterable[Bot]:
        session = AiohttpSession()
        session.middleware(RetryRequestMiddleware())
        async with Bot(
            token=config.token.get_secret_value(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
            session=session,
        ).context() as bot:
            yield bot
