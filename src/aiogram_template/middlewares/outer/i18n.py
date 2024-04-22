from typing import cast

from aiogram.types import User
from aiogram_i18n.managers import BaseManager

from aiogram_template.services.database.models import DBUser


class I18nManager(BaseManager):
    async def get_locale(
        self, event_from_user: User | None = None, db_user: DBUser | None = None
    ) -> str:
        if db_user:
            return db_user.locale
        if event_from_user and event_from_user.language_code is not None:
            return event_from_user.language_code
        return cast(str, self.default_locale)

    async def set_locale(self, locale: str, user: DBUser) -> None:
        user.locale = locale
