from aiogram import Bot

from aiogram_template.settings import Config


def create_bot(config: Config) -> Bot:
    bot = Bot(token=config.common.token.get_secret_value())
    return bot
