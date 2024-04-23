from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from aiogram_template.config import Config
from aiogram_template.utils import mjson


def create_bot(config: Config) -> Bot:
    session = AiohttpSession(json_loads=mjson.decode, json_dumps=mjson.encode)
    bot = Bot(
        token=config.common.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=session,
    )
    return bot
