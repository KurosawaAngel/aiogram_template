from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from aiogram_template.enums import Locale
from aiogram_template.services.database.models import Base


class DBUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, autoincrement=True)
    username: Mapped[str | None] = mapped_column(String(32))
    locale: Mapped[str] = mapped_column(default=Locale.DEFAULT)
