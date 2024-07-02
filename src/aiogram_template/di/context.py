from aiogram import Bot
from dishka import Provider, Scope, from_context


class ContextProvider(Provider):
    scope = Scope.APP

    bot = from_context(provides=Bot)
