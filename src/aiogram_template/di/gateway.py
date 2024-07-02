from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram_template.data.database import gateways as gate


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_user_gateway(self, session: AsyncSession) -> gate.UserGateway:
        return gate.UserGateway(session)
