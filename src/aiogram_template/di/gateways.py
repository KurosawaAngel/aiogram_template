from dishka import Provider, Scope, provide

from aiogram_template.data.database import gateways as gate


class GatewaysProvider(Provider):
    scope = Scope.REQUEST

    user_gateway = provide(gate.UserGateway)
