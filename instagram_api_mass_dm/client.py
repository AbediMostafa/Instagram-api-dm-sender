import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import logging
from typing import Callable
from instagrapi import Client
import pyotp

from instagram_api_mass_dm.exceptions import ProxyNotSetError

logger = logging.getLogger(__name__)


async def run_async(executor, callable: Callable, *args, **kwargs):
    loop = asyncio.get_running_loop()
    func = partial(callable, *args, **kwargs)
    return await loop.run_in_executor(executor, func)


class InstagramAPIWrapper:
    _threadpool: ThreadPoolExecutor
    username: str
    password: str
    proxy: str
    _ip: str

    def __init__(
        self,
        _threadpool: ThreadPoolExecutor,
        username: str = "",
        password: str = "",
        proxy=None,
    ):
        self._threadpool = _threadpool
        self._client = Client()
        self.username = username
        self.password = password

        if proxy:
            self.proxy = proxy
            self._client.set_proxy(proxy)
        self._ip = ""

    async def _send_public_request(
        self,
        url,
        data=None,
        params=None,
        headers=None,
        return_json=False,
        stream=None,
        timeout=None,
        update_headers=None,
    ):
        return await self._run_async(
            self._client._send_public_request,
            url,
            data,
            params,
            headers,
            return_json,
            stream,
            timeout,
            update_headers,
        )

    async def assert_proxy_works(self):
        logger.debug("testing proxy...")
        ip_detector_server = "https://api.ipify.org/"
        self._client.set_proxy("")
        before_ip = await self._send_public_request(ip_detector_server)
        logger.debug(f"before IP: {before_ip}")

        self._client.set_proxy(self.proxy)
        after_ip = await self._send_public_request(ip_detector_server)
        logger.debug(f"after IP: {after_ip}")
        if before_ip == after_ip:
            self._client.set_proxy("")
            raise ProxyNotSetError("Proxy is not set ")
        self._ip = after_ip

    async def _run_async(self, callable: Callable, *args, **kwargs):
        return await run_async(self._threadpool, callable, *args, **kwargs)

    @staticmethod
    def get_verification_code(secret) -> str:
        return pyotp.TOTP(secret).now()

    async def login(self, secret_key=None) -> bool:
        await self.assert_proxy_works()
        kwargs = dict(username=self.username, password=self.password)
        if secret_key:
            kwargs.update(verification_code=self.get_verification_code(secret_key))
        logged_in = await self._run_async(self._client.login, **kwargs)
        logger.info(f"logged in successfully? -> {logged_in}")
        return logged_in
