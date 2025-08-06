import asyncio
import pytest
import pytest_asyncio
from massdm_cache.redis import RedisCache


@pytest_asyncio.fixture(loop_scope="class")
async def redis_cache_fixture(request):
    cache = await RedisCache.create(force_reconnect=True)
    request.cls.cache = cache  # attach to test class
    yield
    await cache.clear()
    await cache.disconnect()


@pytest.mark.asyncio(loop_scope="class")
@pytest.mark.usefixtures("redis_cache_fixture")
class TestRedisCache:
    cache: RedisCache

    async def test_set_and_get(self):
        await self.cache.set("foo", "bar")
        value = await self.cache.get("foo")
        assert value == "bar"

    async def test_get_nonexistent_key(self):
        assert await self.cache.get("missing") is None

    async def test_delete_key(self):
        await self.cache.set("key", "value")
        await self.cache.delete("key")
        assert await self.cache.get("key") is None

    async def test_clear_cache(self):
        await self.cache.set("a", "1")
        await self.cache.set("b", "2")
        await self.cache.clear()
        assert await self.cache.get("a") is None
        assert await self.cache.get("b") is None

    async def test_set_with_ttl(self):
        await self.cache.set("temp", "123", ttl=1)
        value = await self.cache.get("temp")
        assert value == "123"
        await asyncio.sleep(1.2)
        value = await self.cache.get("temp")
        assert value is None

    async def test_connection_pool_reuse(self):
        instance1 = await RedisCache.create()
        pool1 = instance1._redis.connection_pool
        instance2 = await RedisCache.create()
        pool2 = instance2._redis.connection_pool
        await instance1.clear()
        assert pool1 is pool2
        assert instance1._redis is not instance2._redis
