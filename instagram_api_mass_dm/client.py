import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import json
import logging
from typing import Any, Callable
from instagrapi import Client
import pyotp

from instagram_api_mass_dm.consts import CachePrefix
from instagram_api_mass_dm.exceptions import ProxyNotSetError
from instagrapi.exceptions import LoginRequired
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
    _cache: massdm_cache.Cache

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._cache.disconnect()

    def __init__(
        self,
        _threadpool: ThreadPoolExecutor,
        username: str = "",
        password: str = "",
        proxy=None,
        cache: massdm_cache.Cache = None,
        session_life: int = 24 * 60 * 60,
    ):
        self._threadpool = _threadpool
        self._client = Client()
        self.username = username
        self.password = password
        self._cache = cache
        self.session_life = session_life

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

    def login_scenario(self, session: dict = {}, secret: str = ""):
        """
        Attempts to login to Instagram using either the provided session information
        or the provided username and password.
        """
        login_via_session = False
        login_via_pw = False
        cl = self._client
        username, password = self.username, self.password
        if session:
            try:
                cl.set_settings(session)
                cl.login(username, password)

                # check if session is valid
                try:
                    cl.get_timeline_feed()
                except LoginRequired:
                    logger.info(
                        "Session is invalid, need to login via username and password"
                    )
                    old_session = cl.get_settings()
                    # use the same device uuids across logins
                    cl.set_settings({})
                    cl.set_uuids(old_session["uuids"])

                    cl.login(
                        username,
                        password,
                        verification_code=self.get_verification_code(secret),
                    )
                login_via_session = True
            except Exception as e:
                logger.info("Couldn't login user using session information: %s" % e)

        if not login_via_session:
            try:
                logger.info(
                    "Attempting to login via username and password. username: %s"
                    % username
                )
                if cl.login(
                    username,
                    password,
                    verification_code=self.get_verification_code(secret),
                ):
                    login_via_pw = True
            except Exception as e:
                logger.info("Couldn't login user using username and password: %s" % e)

        if not login_via_pw and not login_via_session:
            raise Exception("Couldn't login user with either password or session")
        logger.info(f"login_success: {self.username}")
        return True

    @staticmethod
    def get_verification_code(secret) -> str:
        return pyotp.TOTP(secret).now() if secret else ""

    def get_account_id(self):
        return self._client.user_id

    async def _cache_session(self):
        settings = self._client.get_settings()
        key = CachePrefix.ACCOUNT_SESSION.format(self.username)
        await self._cache.set(key, json.dumps(settings), ttl=self.session_life)

    async def get_session_from_cache(self) -> Any:
        key = CachePrefix.ACCOUNT_SESSION.format(self.username)
        settings = await self._cache.get(key)
        if settings is not None:
            return json.loads(settings)

    async def login(self, secret_key: str = "") -> bool:
        await self.assert_proxy_works()
        session = await self.get_session_from_cache()

        login = lambda: self.login_scenario(session=session, secret=secret_key)
        logged_in = await self._run_async(login)
        if logged_in:
            await self._cache_session()
        return logged_in
