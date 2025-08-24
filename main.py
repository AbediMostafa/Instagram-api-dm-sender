"""
This module is the place that all the other project pacakges(moduels)
can be imported and is the highest level
"""

from concurrent.futures import ThreadPoolExecutor
import logging
from threading import Thread
from db.manager import AccountSelector
from instagram_api_massdm.scheduler import Scheduler
from instagram_api_massdm.workflows import Login
from instagram_api_wrapper.client import InstagramAPIWrapper
from settings import AccountSettings, General
from django.core.cache import cache


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)


def run_jobs(account_selector: AccountSelector):
    while True:
        account = account_selector.get()
        api = InstagramAPIWrapper(
            account.username,
            account.password,
            proxy=General.proxy,
            cache=cache,
            session_life=AccountSettings.session_life,
        )
        Login(api=api, account=account)()


def start():
    selector = AccountSelector(
        buffer_max_size=AccountSettings.buffer_max_size,
        buffer_min_size=AccountSettings.buffer_min_size,
        watch_interval=10,
    )
    selector.fill()
    selector.refresh()  # start the selector
    executor = ThreadPoolExecutor(max_workers=General.max_workers)
    Thread(target=selector.watch_accounts).start()
    for _ in range(General.max_workers):
        executor.submit(run_jobs, selector)


start()
