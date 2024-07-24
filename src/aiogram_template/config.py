from secrets import token_urlsafe
from typing import Self

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", frozen=True
    )


class CommonConfig(BaseConfig, env_prefix="COMMON_"):
    admin_chat_id: int = -1


class BotConfig(BaseConfig, env_prefix="BOT_"):
    drop_pending_updates: bool = True
    token: SecretStr = Field(default="")


class WebhookConfig(BaseConfig, env_prefix="WEBHOOK_"):
    host: str = "127.0.0.1"
    base: str = ""
    path: str = "/webhook"
    port: int = 80
    secret: str = Field(default_factory=token_urlsafe)
    use: bool = False

    @property
    def bot_url(self) -> str:
        """URL for Webhook"""
        return f"{self.base}{self.path}"


class DatabaseConfig(BaseConfig, env_prefix="DATABASE_"):
    url: SecretStr = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost/postgres"
    )


class RedisConfig(BaseConfig, env_prefix="REDIS_"):
    host: str = "localhost"
    port: int = 6379
    database: int = 0

    @property
    def redis_url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.database}"


class Config(BaseModel):
    common: CommonConfig
    webhook: WebhookConfig
    postgres: DatabaseConfig
    redis: RedisConfig
    bot: BotConfig

    @classmethod
    def create(cls) -> Self:
        return cls(
            common=CommonConfig(),
            webhook=WebhookConfig(),
            postgres=DatabaseConfig(),
            redis=RedisConfig(),
            bot=BotConfig(),
        )
