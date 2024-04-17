from dishka import Provider, Scope, from_context

from aiogram_template.config import Config


class ContextProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
