from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.middlewares.register_middleware import register_middleware

from core.config import settings
from core.database.db_helper import db_helper

from api import router as api_router
from core.redis.redis_helper import redis_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_helper.connect()
    yield
    await redis_helper.disconnect()
    await db_helper.dispose()


main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


main_app.include_router(api_router, prefix=settings.api.prefix)
register_middleware(main_app)



if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
    )