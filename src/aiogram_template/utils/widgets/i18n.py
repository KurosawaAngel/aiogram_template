from typing import Dict, cast

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from aiogram_i18n import I18nContext

I18N_FORMAT_KEY = "i18n"


class I18nFormat(Text):
    """Format text via fluent formatting."""

    def __init__(self, key: str, when: WhenCondition = None) -> None:
        super().__init__(when)
        self.key = key

    async def _render_text(self, data: Dict, manager: DialogManager) -> str:
        i18n = cast(I18nContext, manager.middleware_data.get(I18N_FORMAT_KEY))
        return i18n.get(self.key, **data)
