from datetime import datetime

from typing import Sequence

from fastapi import HTTPException

from starlette import status as status_code

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base_repo import BaseRepo

from models import Video

from schemas import (
    VideoCreate,
    VideoUpdate,
    VideoStatusUpdate,
)

from core.redis.redis_helper import redis_helper

from utils import redis_utils


class VideosRepo(BaseRepo[Video, VideoCreate, VideoUpdate]):

    @staticmethod
    async def get_videos_filtered(
            session: AsyncSession,
            status: list[str] | None = None,
            camera_number: list[int] | None = None,
            location: list[str] | None = None,
            start_time_from: datetime | None = None,
            start_time_to: datetime | None = None,
            use_cache: bool = True,
    ) -> Sequence[Video]:
        try:
            filters = {
                "status": status,
                "camera_number": camera_number,
                "location": location,
                "start_time_from": start_time_from,
                "start_time_to": start_time_to,
            }
            cache_key = redis_utils.make_cache_key("videos:", filters)

            if use_cache:
                cached = await redis_helper.get(cache_key)
                if cached:
                    return cached

            query = select(Video).order_by(Video.id)
            if status:
                query = query.where(Video.status.in_(status))
            if camera_number:
                query = query.where(Video.camera_number.in_(camera_number))
            if location:
                query = query.where(Video.location.in_(location))
            if start_time_from:
                query = query.where(Video.start_time >= start_time_from)
            if start_time_to:
                query = query.where(Video.start_time <= start_time_to)
            stmt = await session.execute(query)
            videos = stmt.scalars().all()

            if not videos:
                raise HTTPException(
                    status_code=status_code.HTTP_404_NOT_FOUND,
                    detail="Videos not found",
                )

            if use_cache:
                await redis_helper.set(
                    key=cache_key,
                    value=[video.as_dict() for video in videos],
                    ttl=300,
                )

            return videos

        except Exception as e:
            raise e


    async def get_video_by_id(
            self,
            session: AsyncSession,
            video_id: int,
            use_cache: bool = True,
    ):
        try:
            cache_key = f"videos:{video_id}"
            if use_cache:
                cached = await redis_helper.get(cache_key)
                if cached:
                    return cached

            video = await self.get_by_id(
                session=session,
                model_id=video_id,
            )

            if use_cache:
                await redis_helper.set(
                    key=cache_key,
                    value=video.as_dict(),
                    ttl=300,
                )

            return video

        except Exception as e:
            raise e


    async def create_video(
            self,
            session: AsyncSession,
            create_schema: VideoCreate,
    ):
        try:
            video = await self.create(
                session=session,
                create_schema=create_schema,
            )
            await redis_helper.clear_pattern("videos:*")
            return video

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
            await redis_helper.clear_pattern("videos:*")
            return video

        except Exception as e:
            raise e


videos_repo = VideosRepo(Video)
