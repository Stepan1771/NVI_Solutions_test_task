from sqlalchemy import (
    MetaData,
    DateTime,
    Column,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.functions import func

from core.config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )