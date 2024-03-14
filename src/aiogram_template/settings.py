from secrets import token_urlsafe

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class CommonConfig(BaseSettings, env_prefix="COMMON_"):
    token: SecretStr
    admin_chat_id: int
    drop_pending_updates: bool


class WebhookConfig(BaseSettings, env_prefix="WEBHOOK_"):
    host: str
    base: str
    path: str
    port: int
    secret: SecretStr = Field(default=token_urlsafe)
    reset: bool
    use: bool

    @property
    def webhook_url(self) -> str:
        """URL for Webhook"""
        return f"{self.base}{self.path}"


class PostgresConfig(BaseSettings, env_prefix="POSTGRES_"):
    host: str
    db: str
    password: str
    port: int
    user: str

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class RedisConfig(BaseSettings, env_prefix="REDIS_"):
    host: str
    port: int
    database: int

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.database}"


class Config(BaseSettings):
    common: CommonConfig
    webhook: WebhookConfig
    postgres: PostgresConfig
    redis: RedisConfig

    @property
    def webhook_url(self) -> str:
        return self.webhook.webhook_url

    @property
    def postgres_url(self) -> str:
        return self.postgres.url

    @property
    def redis_url(self) -> str:
        return self.redis.url


def create_config() -> Config:
    return Config(
        common=CommonConfig(),
        webhook=WebhookConfig(),
        postgres=PostgresConfig(),
        redis=RedisConfig(),
    )
