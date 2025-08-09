import asyncio
from concurrent.futures import ThreadPoolExecutor
from instagram_api_mass_dm import InstagramAPIWrapper
import logging

from massdm_cache.redis import RedisCache
import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)


async def main():
    cach = await RedisCache.create()
    async with InstagramAPIWrapper(
        ThreadPoolExecutor(10),
        username=settings.TestAccountData.username,
        password=settings.TestAccountData.password,
        cache=cach,
        proxy=settings.General.PROXY,
    ) as client:
        await client.login(settings.TestAccountData.secret)


if __name__ == "__main__":
    asyncio.run(main())
