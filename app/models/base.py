from datetime import datetime

from sqlalchemy import (
    MetaData,
    DateTime,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)
from sqlalchemy.sql.functions import func

from core.config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )