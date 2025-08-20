import pytest


@pytest.mark.django_db
class TestDatabase:
    def test_account(self, account):
        assert account[0].id

