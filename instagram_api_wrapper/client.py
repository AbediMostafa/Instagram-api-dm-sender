import json
import logging
from pathlib import Path
from typing import Any, Optional
from instagrapi import Client
import pyotp

from instagram_api_wrapper.consts import CachePrefix
from instagram_api_wrapper.exceptions import ProxyNotSetError
from instagrapi.exceptions import LoginRequired

logger = logging.getLogger(__name__)


class InstagramAPIWrapper:
    username: str
    password: str
    proxy: str
    _ip: str
    _cache: Any

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __init__(
        self,
        username: str = "",
        password: str = "",
        proxy=None,
        cache=None,
        session_life: int = 24 * 60 * 60,
    ):
        self._client = Client()
        self.username = username
        self.password = password
        self._cache = cache
        self.session_life_in_cache = session_life

        if proxy:
            self.proxy = proxy
            self._client.set_proxy(proxy)
        else:
            self.proxy = ""
        self._ip = ""

    def _send_public_request(
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
        return self._client._send_public_request(
            url,
            data,
            params,
            headers,
            return_json,
            stream,
            timeout,
            update_headers,
        )

    def assert_proxy_works(self):
        logger.debug("testing proxy...")
        ip_detector_server = "https://api.ipify.org/"
        self._client.set_proxy("")
        before_ip = self._send_public_request(ip_detector_server)
        logger.debug(f"before IP: {before_ip}")

        if not self.proxy:
            raise ProxyNotSetError("No proxy configured")

        self._client.set_proxy(self.proxy)
        after_ip = self._send_public_request(ip_detector_server)
        logger.debug(f"after IP: {after_ip}")
        if before_ip == after_ip:
            self._client.set_proxy("")
            raise ProxyNotSetError("Proxy is not set ")
        self._ip = after_ip

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

    def _cache_session(self):
        if not self._cache:
            return
        settings = self._client.get_settings()
        key = CachePrefix.ACCOUNT_SESSION.format(self.username)
        self._cache.set(key, json.dumps(settings), timeout=self.session_life_in_cache)

    def get_session_from_cache(self) -> Any:
        if not self._cache:
            return None
        key = CachePrefix.ACCOUNT_SESSION.format(self.username)
        settings = self._cache.get(key)
        if settings is not None:
            return json.loads(settings)

    def login(self, secret_key: str = "") -> bool:
        self.assert_proxy_works()
        session = self.get_session_from_cache()
        logged_in = self.login_scenario(session=session, secret=secret_key)
        if logged_in and self._cache:
            self._cache_session()
        return logged_in

    def get_user_id(self, username: str) -> Optional[int]:
        """
        Get the Instagram user ID for a given username.

        Returns:
            int if user exists, None otherwise
        """
        user_id = self._client.user_id_from_username(username)
        return int(user_id)

    def send_dm(
        self,
        user_id: int,
        message: str = "",
        media_path: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> bool:
        """
        Sends a direct message to the specified user_id.
        Optionally sends media (photo or video) along with the message.
        Caches session after sending if cache is enabled.

        media_type: 'photo' or 'video'
        media_path: path to the media file (str or Path)
        """
        try:
            # Convert Path to string if needed
            if media_path:
                media_path = str(media_path)

            # Send media first if provided
            if media_path and media_type:
                if media_type == "photo":
                    self._client.direct_send_photo(
                        path=Path(media_path), user_ids=[user_id]
                    )
                elif media_type == "video":
                    self._client.direct_send_video(
                        path=Path(media_path), user_ids=[user_id]
                    )
                else:
                    logger.error(f"Unsupported media_type: {media_type}")
                    return False

            # Send optional text message
            if message:
                self._client.direct_send(text=message, user_ids=[user_id])

            # Cache session if enabled
            if getattr(self, "_cache", False):
                self._cache_session()

            logger.info(f"DM sent to user_id: {user_id} (media: {media_path})")
            return True

        except Exception as e:
            logger.error(f"Failed to send DM to user_id {user_id}: {e}")
            return False
