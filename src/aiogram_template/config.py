from secrets import token_urlsafe
from typing import Self

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", frozen=True
    )


class CommonConfig(BaseConfig, env_prefix="COMMON_"):
    token: SecretStr = Field(default="")
    admin_chat_id: int = -1
    drop_pending_updates: bool = True


class WebhookConfig(BaseConfig, env_prefix="WEBHOOK_"):
    host: str = "localhost"
    base: str = ""
    path: str = "/webhook"
    port: int = 80
    secret: SecretStr = Field(default_factory=token_urlsafe)
    reset: bool = True
    use: bool = False

    @property
    def url(self) -> str:
        """URL for Webhook"""
        return f"{self.base}{self.path}"


class PostgresConfig(BaseConfig, env_prefix="POSTGRES_"):
    host: str = "localhost"
    db: str = "postgres"
    password: str = "postgres"
    port: int = 5432
    user: str = "postgres"

    @property
    def url(self) -> URL:
        return URL.create(
            "postgresql+asyncpg",
            self.user,
            self.password,
            self.host,
            self.port,
            self.db,
        )


class RedisConfig(BaseConfig, env_prefix="REDIS_"):
    host: str = "localhost"
    port: int = 6379
    database: int = 0

    @property
    def fsm_url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.database}"


class Config(BaseModel):
    common: CommonConfig
    webhook: WebhookConfig
    postgres: PostgresConfig
    redis: RedisConfig

    @property
    def webhook_url(self) -> str:
        return self.webhook.url

    @property
    def database_url(self) -> URL:
        return self.postgres.url

    @property
    def redis_fsm_url(self) -> str:
        return self.redis.fsm_url

    @classmethod
    def create(cls) -> Self:
        return cls(
            common=CommonConfig(),
            webhook=WebhookConfig(),
            postgres=PostgresConfig(),
            redis=RedisConfig(),
        )
