from dishka import Provider, Scope, from_context, provide

from aiogram_template.config import (
    CommonConfig,
    Config,
    DatabaseConfig,
    RedisConfig,
    TelegramConfig,
    WebhookConfig,
)


class ConfigProvider(Provider):
    scope = Scope.APP

    config = from_context(provides=Config)

    @provide
    def get_db_config(self, config: Config) -> DatabaseConfig:
        return config.database

    @provide
    def get_bot_config(self, config: Config) -> TelegramConfig:
        return config.telegram

    @provide
    def get_webhook_config(self, config: Config) -> WebhookConfig:
        return config.webhook

    @provide
    def get_redis_config(self, config: Config) -> RedisConfig:
        return config.redis

    @provide
    def get_common_config(self, config: Config) -> CommonConfig:
        return config.common
