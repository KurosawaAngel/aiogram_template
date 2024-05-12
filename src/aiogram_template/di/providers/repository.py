from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram_template.services.database.repositories import UserRepository


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)
