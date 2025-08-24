from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
import logging
import os
import pickle
from queue import Queue
import time
from typing import Optional

from django.db.models.query import QuerySet
from django.db.transaction import atomic
from django.utils.timezone import now
from db.models import Account, DmPost, Lead

logger = logging.getLogger(__name__)


@dataclass
class LeadMessage:
    id: int
    instagram_id: Optional[int]
    dm_post_id: int
    spintax: Optional[str]
    media_id: Optional[str]


class MessageManager:
    def get_messages(self, user_id, last_command_send_date: datetime):
        return (
            Lead.objects.filter(
                user_id=user_id, last_command_send_date__lt=last_command_send_date
            )
            .build_messages()
            .defer("account", "user", "last_command_send_date")
            .iterator()
        )

    def get_text(self, message: LeadMessage):
        return DmPost.objects.get(id=message.dm_post_id)


class AccountSelector:
    _account_buffer: Queue[Account]
    buffer_size: int
    account_filters: dict
    __filled: bool
    _account_buffer: Queue[Account] = Queue()
    _STARTED = False
    watch_interval: int

    def __init__(
        self,
        account_filters: dict = dict(),
        buffer_min_size=200,
        buffer_max_size=1000,
        backup_path="account_queue.pickle",
        watch_interval=60 * 15,
    ) -> None:
        self.account_filters = account_filters
        self.buffer_size = buffer_min_size
        self.__class__._account_buffer = Queue(maxsize=buffer_max_size)
        self.backup_path = backup_path
        self.watch_interval = watch_interval
        if not self.__class__._STARTED:
            if os.path.exists(backup_path) and os.path.getsize(backup_path):
                with open(backup_path, "rb") as f:
                    backup = pickle.load(f)
                    for a in backup:
                        self.__class__._account_buffer.put(a)
            self.__class__._STARTED = True

    def select_ready_accounts(self, lock=False) -> QuerySet[Account, Account]:
        qs = Account.objects.filter(
            next_login__lte=now(), is_active=1, is_used=0, **self.account_filters
        )
        if lock:
            with atomic():
                pks = list(qs.values_list("pk", flat=True))
                qs = qs.select_for_update()
                qs.update(is_used=1, used_at=now())
                qs = Account.objects.filter(pk__in=pks)
        return qs

    def fill(self, count=None):
        qs = self.select_ready_accounts(lock=True)
        if qs.exists():
            for a in qs[: count or self.buffer_size].iterator():
                self._account_buffer.put(a)

    @property
    def accounts(self) -> Queue[Account]:
        return self._account_buffer

    def get(self) -> Account:
        new_var = self._account_buffer.get()
        print(
            f"--------------------------------------------{new_var, self.accounts.qsize()}\n\n"
        )
        return new_var

    def _backup(self):
        with open(self.backup_path, "wb") as f:
            with self._account_buffer.mutex:
                q_list = list(self._account_buffer.queue)
            if q_list:
                pickle.dump(q_list, f)

    def refresh(self):
        logger.debug("Is refreshing...")
        if self._account_buffer.qsize() <= self.buffer_size:
            self.fill()
            logger.debug(
                f"Refilled!!!!!!!!!!!!!!!!!!!!!!!!!!! LEN: {self.accounts.qsize()}"
            )
            self._backup()

    def watch_accounts(self):
        while True:
            self.refresh()
            time.sleep(self.watch_interval)
