from aiogram import Bot
from aiogram_i18n.cores import FluentRuntimeCore
from dishka import Provider, Scope, from_context


class ContextProvider(Provider):
    scope = Scope.APP

    bot = from_context(provides=Bot)
    fluent = from_context(provides=FluentRuntimeCore)
