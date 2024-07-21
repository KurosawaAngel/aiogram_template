from dishka import Provider, Scope, from_context, provide

from aiogram_template.config import (
    BotConfig,
    CommonConfig,
    Config,
    DatabaseConfig,
    RedisConfig,
    WebhookConfig,
)


class ConfigProvider(Provider):
    scope = Scope.APP

    config = from_context(provides=Config)

    @provide
    def get_db_config(self, config: Config) -> DatabaseConfig:
        return config.postgres

    @provide
    def get_bot_config(self, config: Config) -> BotConfig:
        return config.bot

    @provide
    def get_webhook_config(self, config: Config) -> WebhookConfig:
        return config.webhook

    @provide
    def get_redis_config(self, config: Config) -> RedisConfig:
        return config.redis

    @provide
    def get_common_config(self, config: Config) -> CommonConfig:
        return config.common
