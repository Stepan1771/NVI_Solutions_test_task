import json
from typing import Any, Optional

from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool


class BaseRedisClient:
    def __init__(
            self,
            url: str
    ) -> None:
        self.url = url
        self.pool = ConnectionPool.from_url(
            url=self.url,
            max_connections=10,
            decode_responses=True,
        )
        self.redis: Redis | None = None


    async def connect(self) -> None:
        self.redis = Redis(connection_pool=self.pool)


    async def disconnect(self) -> None:
        if self.redis:
            await self.redis.close()


    async def get(self, key: str) -> Optional[Any]:
        """Получить данные из кэша"""
        if not self.redis:
            return None

        data = await self.redis.get(key)
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return data
        return None


    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Сохранить данные в кэш"""
        if not self.redis:
            return False

        if isinstance(value, (dict, list, tuple)):
            value = json.dumps(value, ensure_ascii=False)

        return await self.redis.setex(key, ttl, value)


    async def delete(self, key: str) -> bool:
        """Удалить ключ из кэша"""
        if not self.redis:
            return False
        return await self.redis.delete(key)


    async def clear_pattern(self, pattern: str) -> int:
        """Удалить все ключи по паттерну"""
        if not self.redis:
            return 0

        keys = await self.redis.keys(pattern)
        if keys:
            return await self.redis.delete(*keys)
        return 0