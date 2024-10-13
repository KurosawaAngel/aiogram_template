from typing import AsyncIterable

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dishka import Provider, Scope, provide

from aiogram_template.config import TelegramConfig


class BotProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_bot(self, config: TelegramConfig) -> AsyncIterable[Bot]:
        async with Bot(
            token=config.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        ) as bot:
            yield bot
