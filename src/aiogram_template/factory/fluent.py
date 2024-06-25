from aiogram_i18n.cores import FluentRuntimeCore

from aiogram_template.enums.locale import Locale


def setup_fluent_core() -> FluentRuntimeCore:
    return FluentRuntimeCore(
        path="translations/{locale}",
        raise_key_error=False,
        default_locale=Locale.DEFAULT,
    )
