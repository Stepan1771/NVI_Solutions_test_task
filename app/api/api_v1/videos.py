from datetime import datetime

from typing import (
    List,
    Annotated,
)

from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
)

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status

from core.config import settings
from core.database.db_helper import db_helper

from repositories.videos_repo import videos_repo

from schemas import (
    VideoCreate,
    VideoStatusUpdate,
)
from schemas.video import VideoRead


router = APIRouter(
    prefix=settings.api.v1.videos,
    tags=["Videos"],
)


@router.get(
    path="",
    summary="Получить список всех видео с поддержкой фильтров",
    response_model=List[VideoRead],
    status_code=status.HTTP_200_OK,
)
async def get_videos(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        status: List[str] | None = Query(None),
        camera_number: List[int] | None = Query(None),
        location: List[str] | None = Query(None),
        start_time_from: datetime | None = Query(None),
        start_time_to: datetime | None = Query(None),
):
    videos = await videos_repo.get_videos_filtered(
        session=session,
        status=status,
        camera_number=camera_number,
        location=location,
        start_time_from=start_time_from,
        start_time_to=start_time_to,
    )
    return [
        VideoRead.model_validate(video) for video in videos
    ]


@router.get(
    path="/{video_id}",
    summary="Получить информацию по конкретному видео по ID",
    response_model=VideoRead,
    status_code=status.HTTP_200_OK,
)
async def get_video_by_id(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        video_id: int = Path(..., description="ID видео"),
):
    video = await videos_repo.get_by_id(
        session=session,
        model_id=video_id,
    )
    return VideoRead.model_validate(video)


@router.post(
    path="",
    summary="Добавить новое видео",
    response_model=VideoRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_video(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        create_schema: VideoCreate,
):
    video = await videos_repo.create(
        session=session,
        create_schema=create_schema,
    )
    return VideoRead.model_validate(video)


@router.patch(
    path="/{video_id}/status",
    summary="Обновить статус видео",
    response_model=VideoRead,
    status_code=status.HTTP_200_OK,
)
async def update_video_status(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        update_schema: VideoStatusUpdate,
        video_id: int = Path(..., description="ID видео"),
):
    video = await videos_repo.update_status(
        session=session,
        update_schema=update_schema,
        video_id=video_id,
    )
    return VideoRead.model_validate(video)