from datetime import timedelta
from typing import Optional, Self
import redis.asyncio as redis


from massdm_cache.cache import Cache


class RedisCache(Cache):
    __connection_pool: dict[str, redis.ConnectionPool] = {}

    def __init__(self, redis: redis.Redis):
        self._redis = redis

    @classmethod
    async def create(
        cls,
        *,
        redis_url: str = "redis://localhost:6379/0",
        force_reconnect: bool = False,
        max_connections: int = 10
    ) -> Self:
        connection = cls.__connection_pool.get(redis_url)
        if connection and not force_reconnect:
            return cls(redis.Redis(connection_pool=connection))
        redis_connection = await redis.from_url(
            redis_url, max_connections=max_connections
        )
        cls.__connection_pool[redis_url] = redis_connection.connection_pool
        return cls(redis_connection)

    async def get(self, key):
        value = await self._redis.get(key)
        return value.decode("utf-8") if value else None

    async def set(self, key, value, ttl=None):
        if ttl:
            await self._redis.set(key, value, ex=timedelta(seconds=ttl))
        else:
            await self._redis.set(key, value)

    async def delete(self, key):
        await self._redis.delete(key)

    async def clear(self):
        await self._redis.flushdb()

    async def disconnect(self):
        await self._redis.close()
