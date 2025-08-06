import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import json
import logging
import os
from typing import Callable
from instagrapi import Client
import pyotp

from instagram_api_mass_dm.exceptions import ProxyNotSetError
import massdm_cache

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
        cache: massdm_cache.Cache | None = None,
        proxy=None,
    ):
        self._threadpool = _threadpool
        self._client = Client()
        self.username = username
        self.password = password
        self._cache = cache
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

    async def _cache_session(self):
        settings = self._client.get_settings()
        self._cache

    async def _set_session_from_cache(self):
        if os.path.exists("username.json"):
            session = json.load(open("username.json", "r"))
            self._client.set_settings(session)

    async def login(self, secret_key=None, use_cache=True) -> bool:
        await self.assert_proxy_works()
        await self._set_session_from_cache()
        kwargs = dict(username=self.username, password=self.password)
        if secret_key:
            kwargs.update(verification_code=self.get_verification_code(secret_key))
        async_login = self._run_async(self._client.login, **kwargs)
        logged_in = await async_login
        if logged_in:
            await self._cache_session()
        logger.info(f"logged in successfully? -> {logged_in}")
        return logged_in
