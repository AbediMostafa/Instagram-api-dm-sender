
from typing import Sequence
import pytest
from model_bakery import baker
from db.models import Account, DmPost, User


pytest_plugins = ["pytest_django"]

def _create_mock_objects(reuqest: pytest.FixtureRequest, model):
    kwargs_tuple = getattr(reuqest, "param", tuple())
    if len(kwargs_tuple) == 0:
        kwargs_tuple = [{}]
    return [baker.make(model, **kwargs) for kwargs in kwargs_tuple]


# ------------------
# Model Fixtures
# ------------------
def user(request: pytest.FixtureRequest):
    yield _create_mock_objects(request, User)


@pytest.fixture
def account(request: pytest.FixtureRequest):
    yield _create_mock_objects(request, Account)


# -----------------
# DmPost fixture
# -----------------
@pytest.fixture
async def dm_post(request: pytest.FixtureRequest):
    yield _create_mock_objects(request, DmPost)
