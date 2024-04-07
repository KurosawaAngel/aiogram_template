from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram_template.config import Config


def create_bot(config: Config) -> Bot:
    bot = Bot(
        token=config.common.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    return bot
