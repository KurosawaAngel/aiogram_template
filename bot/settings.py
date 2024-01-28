import secrets

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Env settings for bot"""

    token: SecretStr
    admin_chat_id: int
    use_webhook: bool
    use_redis: bool
    drop_pending_updates: bool

    postgres_host: str
    postgres_db: str
    postgres_password: str
    postgres_port: int
    postgres_user: str

    webhook_host: str
    webhook_base: str
    webhook_path: str
    webhook_port: int
    secret: str = Field(default_factory=secrets.token_urlsafe())
    reset_webhook: bool

    redis_host: str
    redis_port: int
    redis_database: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def postgres_url(self):
        """URL for DataBase"""
        return (
            "postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def webhook_url(self):
        return f"{self.webhook_base}{self.webhook_path}"
