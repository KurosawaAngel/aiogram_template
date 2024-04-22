from aiogram import Bot, Dispatcher
from dishka import AsyncContainer

from aiogram_template.config import Config


async def on_startup(bot: Bot, config: Config, dispatcher: Dispatcher) -> None:
    if config.webhook.use:
        await bot.set_webhook(
            config.webhook_url,
            drop_pending_updates=config.common.drop_pending_updates,
            secret_token=config.webhook.secret.get_secret_value(),
            allowed_updates=dispatcher.resolve_used_update_types(),
        )
        return
    await bot.delete_webhook(drop_pending_updates=config.common.drop_pending_updates)


async def on_shutdown(bot: Bot, config: Config, main_container: AsyncContainer) -> None:
    if config.webhook.reset:
        await bot.delete_webhook()
    await bot.session.close()
    await main_container.close()
