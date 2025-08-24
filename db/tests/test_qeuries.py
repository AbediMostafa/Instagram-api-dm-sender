import os
from django.utils.timezone import now
from model_bakery import baker
import pytest

from db import models
from db.manager import AccountSelector


@pytest.mark.django_db
class TestDatabase:
    def test_account(self, account):
        assert account[0].id

    def test_get_messages(self):
        dm_posts = [baker.prepare("db.DmPost", priority=i) for i in [1, 1, 1, 2, 2]]
        leads = [baker.prepare("db.Lead", times=i) for i in [0, 0, 0, 1, 2]]
        leads = models.Lead.objects.bulk_create(leads)
        msgs = models.Lead.objects.build_messages()
        assert msgs.exists()


@pytest.mark.django_db
class TestAccountSelector:
    def setup_method(self):
        baker.make(
            models.Account,
            _quantity=5,
            is_active=1,
            is_used=0,
            next_login=now(),
            _bulk_create=True,
            _fill_optional=False,
        )

    def test_fill(self, account_selector: AccountSelector):
        account_selector.fill(3)
        assert account_selector.accounts.qsize() == 3

    def test_refresh_and_get(self, account_selector: AccountSelector):
        account_selector.fill(3)
        for _ in range(3):
            a = account_selector.get()
            assert isinstance(a, models.Account)
        assert account_selector.accounts.qsize() == 0
        account_selector.fill()
        assert account_selector.accounts.qsize() == 5

    def test_select_with_lock(self, account_selector: AccountSelector):
        assert account_selector.select_ready_accounts(lock=True)[0].is_used

    def test_refresh(self, account_selector: AccountSelector):
        account_selector.refresh()
        assert os.path.exists(account_selector.backup_path)
