import tomllib
from dataclasses import dataclass, field
from secrets import token_urlsafe

from adaptix import Retort


@dataclass(slots=True, frozen=True)
class CommonConfig:
    admin_chat_id: int


@dataclass(slots=True, frozen=True)
class TelegramConfig:
    token: str
    drop_pending_updates: bool


@dataclass(slots=True, frozen=True)
class DatabaseConfig:
    url: str


@dataclass(slots=True, frozen=True)
class RedisConfig:
    url: str


@dataclass(slots=True, frozen=True)
class WebhookConfig:
    host: str
    base: str
    port: int
    use: bool
    secret: str = field(default_factory=token_urlsafe)

    @property
    def bot_url(self) -> str:
        return f"{self.base}/bot"


@dataclass(slots=True, frozen=True)
class Config:
    redis: RedisConfig
    database: DatabaseConfig
    common: CommonConfig
    webhook: WebhookConfig
    telegram: TelegramConfig


def load_config() -> Config:
    with open("config.toml", "rb") as f:
        data = tomllib.load(f)

    retort = Retort()

    return retort.load(data, Config)
