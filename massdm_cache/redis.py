from datetime import timedelta
from random import randint
from typing import Optional, Self
import redis.asyncio as redis


from massdm_cache.cache import Cache


class RedisCache(Cache):
    __connection_pool: dict[str, redis.ConnectionPool] = {}

    def __init__(self, redis: redis.Redis, default_cache_approximation=0.1):
        self._redis = redis
        self.default_cache_approximation = default_cache_approximation

    @classmethod
    async def create(
        cls,
        *,
        redis_url: str = "redis://localhost:6379/0",
        force_reconnect: bool = False,
        max_connections: int = 10,
        default_cache_approximation=0.1
    ) -> Self:
        connection = cls.__connection_pool.get(redis_url)
        if connection and not force_reconnect:
            return cls(redis.Redis(connection_pool=connection))
        redis_connection = await redis.from_url(
            redis_url, max_connections=max_connections
        )
        cls.__connection_pool[redis_url] = redis_connection.connection_pool  # type: ignore
        return cls(redis_connection, default_cache_approximation)

    async def get(self, key):
        value = await self._redis.get(key)
        return value.decode("utf-8") if value else None

    async def set(self, key, value, ttl=None, approximate=True):
        if ttl:
            if approximate:
                ttl = randint(
                    ttl * (1 - self.default_cache_approximation),
                    ttl * (1 + self.default_cache_approximation),
                )
            await self._redis.set(key, value, ex=timedelta(seconds=ttl))
        else:
            await self._redis.set(key, value)

    async def delete(self, key):
        await self._redis.delete(key)

    async def clear(self):
        await self._redis.flushdb()

    async def disconnect(self):
        await self._redis.close()
