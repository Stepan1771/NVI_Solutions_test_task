from fastapi import APIRouter

from core.config import settings

from .videos import router as videos_router


router = APIRouter(
    prefix=settings.api.v1.prefix,
)


router.include_router(videos_router)
