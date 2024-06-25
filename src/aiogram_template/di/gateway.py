from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram_template.services.database import gateways as repo


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_user_gateway(self, session: AsyncSession) -> repo.UserGateway:
        return repo.UserGateway(session)
