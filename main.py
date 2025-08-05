import asyncio
from concurrent.futures import ThreadPoolExecutor
from instagram_api_mass_dm import InstagramAPIWrapper
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)


client = InstagramAPIWrapper(
    ThreadPoolExecutor(10),
    username="fardamotors.2103__k",
    password="cq0lhfrz3j60ecpk",
    proxy="http://germanproxy42de:HxxDt7rfpwWn@x462.fxdx.in:13916",
)

if __name__ == "__main__":
    asyncio.run(client.login("rvlndfbpbmqgbykhrxbqjdin6lc55pqe"))
