from aiogram_i18n.cores import FluentRuntimeCore
from dishka import Provider, Scope, provide

from aiogram_template.enums import Locale


class FluentProvider(Provider):
    scope = Scope.APP

    @provide
    def get_fluent(self) -> FluentRuntimeCore:
        return FluentRuntimeCore(
            path="translations/{locale}",
            raise_key_error=False,
            default_locale=Locale.DEFAULT,
        )
