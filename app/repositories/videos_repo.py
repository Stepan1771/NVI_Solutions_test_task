from datetime import datetime

from typing import Sequence

from fastapi import HTTPException

from starlette import status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base_repo import BaseRepo

from models import Video

from schemas import (
    VideoCreate,
    VideoUpdate,
    VideoStatusUpdate,
)


class VideosRepo(BaseRepo[Video, VideoCreate, VideoUpdate]):

    @staticmethod
    async def get_videos_filtered(
            session: AsyncSession,
            video_status: list[str] | None = None,
            camera_number: list[int] | None = None,
            location: list[str] | None = None,
            start_time_from: datetime | None = None,
            start_time_to: datetime | None = None,
    ) -> Sequence[Video]:
        try:
            query = select(Video).order_by(Video.id)
            if status:
                query = query.where(Video.status.in_(video_status))
            if camera_number:
                query = query.where(Video.camera_number.in_(camera_number))
            if location:
                query = query.where(Video.location.in_(location))
            if start_time_from:
                query = query.where(Video.start_time >= start_time_from)
            if start_time_to:
                query = query.where(Video.start_time <= start_time_to)
            stmt = await session.execute(query)
            results = stmt.scalars().all()
            if not results:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Videos not found",
                )
            return results

        except Exception as e:
            raise e


    async def update_status(
            self,
            session: AsyncSession,
            update_schema: VideoStatusUpdate,
            video_id: int,
    ) -> Video:
        try:
            video = await self.get_by_id(
                session=session,
                model_id=video_id,
            )
            video.status = update_schema.status
            session.add(video)
            await session.commit()
            await session.refresh(video)
            return video

        except Exception as e:
            raise e


videos_repo = VideosRepo(Video)
