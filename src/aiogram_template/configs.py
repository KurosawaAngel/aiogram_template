from secrets import token_urlsafe
from typing import Self

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict


class BaseConfig(_BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", frozen=True
    )


class CommonConfig(BaseConfig, env_prefix="COMMON_"):
    token: SecretStr
    admin_chat_id: int
    drop_pending_updates: bool


class WebhookConfig(BaseConfig, env_prefix="WEBHOOK_"):
    host: str
    base: str
    path: str
    port: int
    secret: SecretStr = Field(default=token_urlsafe)
    reset: bool
    use: bool

    @property
    def url(self) -> str:
        """URL for Webhook"""
        return f"{self.base}{self.path}"


class PostgresConfig(BaseConfig, env_prefix="POSTGRES_"):
    host: str
    db: str
    password: str
    port: int
    user: str

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class RedisConfig(BaseConfig, env_prefix="REDIS_"):
    host: str
    port: int
    database: int

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.database}"


class Config(BaseConfig):
    common: CommonConfig
    webhook: WebhookConfig
    postgres: PostgresConfig
    redis: RedisConfig

    @property
    def webhook_url(self) -> str:
        return self.webhook.url

    @property
    def database_url(self) -> str:
        return self.postgres.url

    @property
    def redis_url(self) -> str:
        return self.redis.url

    @classmethod
    def create_config(cls) -> Self:
        return cls(
            common=CommonConfig(),
            webhook=WebhookConfig(),
            postgres=PostgresConfig(),
            redis=RedisConfig(),
        )
