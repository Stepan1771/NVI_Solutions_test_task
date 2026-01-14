from core.config import settings
from core.redis.base import BaseRedisClient


class RedisHelper(BaseRedisClient):
    pass


redis_helper = RedisHelper(
    url=settings.redis.url,
)