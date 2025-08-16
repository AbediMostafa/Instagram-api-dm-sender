from datetime import datetime, timedelta
import pytest
import models
from models.tests.conftest import TestDatabase


# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "account",
#     [[
#         {"next_login": datetime.now() - timedelta(minutes=100), "is_used": 0},
#         {"next_login": datetime.now() + timedelta(minutes=5), "is_used": 0},
#         {"next_login": datetime.now() - timedelta(minutes=1), "is_used": 1},
#         {"next_login": datetime.now() - timedelta(minutes=4), "is_used": 0},
#     ]],
#     indirect=True,
# )
# async def test_inactivate_devices(db, account):
#     ready_accounts = await models.Account.pick_ready_ones()
#     assert len(ready_accounts) == 1


@pytest.mark.asyncio
class TestSelectors(TestDatabase):

    @pytest.mark.parametrize(
        "account",
        [
            (
                {"next_login": datetime.now() - timedelta(minutes=100), "is_used": 0},
                {"next_login": datetime.now() + timedelta(minutes=5), "is_used": 0},
                {"next_login": datetime.now() - timedelta(minutes=1), "is_used": 1},
                {"next_login": datetime.now() - timedelta(minutes=4), "is_used": 0},
            )
        ],
        indirect=True,
    )
    async def test_pick_ready_ones(self, account):
        ready_accounts = await models.Account.pick_ready_ones()
        assert len(ready_accounts) == 2
