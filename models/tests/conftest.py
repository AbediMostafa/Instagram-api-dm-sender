from datetime import datetime
import pytest
import pytest_asyncio
from tortoise import Tortoise
from models.base import init
from models.models import Account
import settings
from faker import Faker


from tortoise import Tortoise


@pytest_asyncio.fixture
async def db():
    kwargs = {
        k: getattr(settings.TestDatabase, k)
        for k in dir(settings.TestDatabase)
        if not k.startswith("_")
    }
    await init(**kwargs, migrate_schema=True)
    yield
    await teardownModels()


fake = Faker()


@pytest_asyncio.fixture
async def account(request: pytest.FixtureRequest):
    kwargs_tuple = request.param
    accounts = []
    kwargs_dict = dict(
        proxy=fake.random_int(min=1000, max=9999),
        color=fake.random_int(min=0, max=16777215),  # RGB range
        screen_resolution=fake.random_int(min=720, max=2160),
        profile=fake.random_int(min=1, max=1000),
        category=fake.random_int(min=1, max=20),
        secret_key=fake.uuid4(),
        username=fake.user_name(),
        password=fake.password(),
        name=fake.name(),
        bio=fake.sentence(nb_words=10),
        email=fake.email(),
        profile_pic_url=fake.image_url(),
        instagram_state=fake.random_element(elements=["active", "inactive", "banned"]),
        app_state=fake.random_element(elements=["idle", "busy"]),
        avatar_changed=fake.random_int(min=0, max=1),
        username_changed=fake.random_int(min=0, max=1),
        initial_posts_deleted=fake.random_int(min=0, max=1),
        has_enough_posts=fake.random_int(min=0, max=1),
        is_used=fake.random_int(min=0, max=1),
        is_active=fake.random_int(min=0, max=1),
        is_public=fake.random_int(min=0, max=1),
        web_session=fake.uuid4(),
        mobile_session=fake.uuid4(),
        log=fake.text(max_nb_chars=200),
        updated_at=datetime.now(),
        next_login=datetime.now(),
    )
    for kwargs in kwargs_tuple:
        kwargs_dict.update(kwargs)
        accounts.append(Account(**kwargs_dict))

    yield await Account.bulk_create(accounts)


async def drop_all_tables():
    try:
        conn = Tortoise.get_connection("default")
        # Fetch all tables
        tables = await conn.execute_query_dict(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
        )
        # Drop each table
        for table in tables:
            await conn.execute_script(
                f'DROP TABLE IF EXISTS "{table["table_name"]}" CASCADE;'
            )
    except Exception as e:
        print(f"Error during drop_all_tables: {e}")
        raise


async def teardownModels():
    await drop_all_tables()
    # Only close connections if you're sure no other test is using them


@pytest.mark.asyncio
@pytest.mark.usefixtures("db")
class TestDatabase:
    pass
