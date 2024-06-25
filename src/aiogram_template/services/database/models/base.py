from datetime import datetime

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    type_annotation_map = {datetime: TIMESTAMP(timezone=True)}

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
