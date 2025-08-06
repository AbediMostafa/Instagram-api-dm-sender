import asyncio
from concurrent.futures import ThreadPoolExecutor
from instagram_api_mass_dm import InstagramAPIWrapper
import logging

from massdm_cache.redis import RedisCache

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)




async def main():
    cach = await RedisCache.create()
    async with InstagramAPIWrapper(
        ThreadPoolExecutor(10),
        username="fardamotors.2103__k",
        password="cq0lhfrz3j60ecpk", 
        cache=cach,
        proxy="http://germanproxy42de:HxxDt7rfpwWn@x462.fxdx.in:13916",
    ) as client:
        await client.login("rvlndfbpbmqgbykhrxbqjdin6lc55pqe")
if __name__ == "__main__":
    asyncio.run(main())
