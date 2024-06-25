from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from aiogram_template.config import BotConfig
from aiogram_template.middlewares.request import RetryRequestMiddleware
from aiogram_template.utils import mjson


def setup_bot(config: BotConfig) -> Bot:
    session = AiohttpSession(json_loads=mjson.decode, json_dumps=mjson.encode)
    session.middleware(RetryRequestMiddleware())
    return Bot(
        token=config.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=session,
    )
