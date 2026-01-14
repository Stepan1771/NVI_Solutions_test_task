from datetime import (
    datetime,
    timedelta,
)

from sqlalchemy import (
    String,
    DateTime,
    Integer,
    Interval,
)
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
)

from . import Base
from .mixins import IntIdPkMixin


class Video(Base, IntIdPkMixin):
    __tablename__ = "videos"

    video_path: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    start_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    duration: Mapped[timedelta] = mapped_column(
        Interval,
        nullable=False,
    )
    camera_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    location: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="new"
    )

    def as_dict(self):
        return {
            "id": self.id,
            "video_path": self.video_path,
            "start_time": self.start_time,
            "duration": self.duration,
            "camera_number": self.camera_number,
            "location": self.location,
            "status": self.status,
            "created_at": self.created_at,
        }
