from datetime import (
    datetime,
    timedelta,
)

from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
    Field,
)


class VideoBase(BaseModel):

    @field_validator("video_path")
    @classmethod
    def validate_video_path(
            cls,
            value: str,
    ) -> str:
        if not value.strip():
            raise ValueError("video_path не должен быть пустым")
        return value

    @field_validator("location")
    @classmethod
    def validate_location(
            cls,
            value: str,
    ) -> str:
        if not value.strip():
            raise ValueError("location не должна быть пустой")
        return value

    @field_validator("duration")
    @classmethod
    def validate_duration(
            cls,
            value: timedelta,
    ) -> timedelta:
        if value.total_seconds() <= 0:
            raise ValueError("duration должен быть положительным")
        return value


class VideoCreate(VideoBase):
    video_path: str = Field(..., min_length=1)
    start_time: datetime
    duration: timedelta
    camera_number: int = Field(..., gt=0)
    location: str = Field(..., min_length=1)
    status: Literal["new", "transcoded", "recognized"] = "new"


class VideoUpdate(VideoBase):
    video_path: str | None = Field(None, min_length=1)
    start_time: datetime | None = None
    duration: timedelta | None = None
    camera_number: int | None = Field(None, gt=0)
    location: str | None = Field(None, min_length=1)
    status: Literal["new", "transcoded", "recognized"] | None = None


class VideoStatusUpdate(VideoBase):
    status: Literal["new", "transcoded", "recognized"]


class VideoRead(VideoBase):
    id: int
    video_path: str
    start_time: datetime
    duration: timedelta
    camera_number: int
    location: str
    status: Literal["new", "transcoded", "recognized"]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )