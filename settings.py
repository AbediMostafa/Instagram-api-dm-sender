import multiprocessing
from pathlib import Path
from os import getenv


class TestAccountData:
    username = getenv("MASSDM_TEST_ACCOUNT_USERNAME", "choob_lab_style")
    password = getenv("MASSDM_TEST_ACCOUNT_PASSWORD", "i39vflh7dmsfldf25")
    secret = getenv("MASSDM_TEST_ACCOUNT_SECRET", "6exvtnvolefjwqq7etlkjuh25qle2bv7")


class Mode:
    test = "TEST"
    debug = "DEBUG"
    production = "PRO"


num_cpus = multiprocessing.cpu_count()


class General:
    proxy = getenv(
        "MASSDM_PROXY",
        "239c1e03149f4688d9b7__cr.de:d4c552dfbab2110c@gw.dataimpulse.com:10003",
    )
    runtime_mode = getenv("MASSDM_RUNITME_MODE", Mode.test)
    max_workers = int(getenv("MASSDM_MAX_WORKERS", num_cpus * 3))

def string_int_to_list(string):
    return [int(i) for i in string.split(',')]

class Sleep:
    before_login = string_int_to_list(getenv("MASSDM_SLEEP_BEFORE_LOGIN", '10,20'))


class Cache:
    default = getenv("MASSDM_CACHE_URL", "redis://localhost:6379/0")


class Database:
    host = getenv("MASSDM_DB_HOST", "localhost")
    port = getenv("MASSDM_DB_HOST", "5434")
    database = getenv("MASSDM_DB_NAME", "instagram_dm_sender")
    user = getenv("MASSDM_DB_USER", "postgres")
    password = getenv("MASSDM_DB_PASSWORD", "arka")
    min_connections = int(getenv("MASSDM_DB_MIN_CONNECTIONS", "5"))
    max_connections = int(getenv("MASSDM_DB_MAX_CONNECTIONS", "60"))


class TestDatabase(Database):
    database = getenv("MASSDM_DB_NAME", "test_instagram_dm_sender")


class AccountSettings:
    buffer_min_size = int(getenv("MASSDM_ACCOUNT_BUFFER_MAX_SIZE", 200))
    buffer_max_size = int(getenv("MASSDM_ACCOUNT_BUFFER_MIN_SIZE", 300))
    session_life = int(getenv("MASSDM_ACCOUNT_SESSION_LIFE", 24 * 60 * 60))


if getenv("PYTEST_CURRENT_TEST"):
    General.runtime_mode = Mode.test


def is_testing():
    return General.runtime_mode == Mode.test


BASE_DIR = Path(__file__).resolve().parent

INSTALLED_APPS = ["db.apps.DbConfig", "django_apscheduler"]

TEST_DB = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": ":memory:",  # in-memory DB for fast tests
}
DB = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": getenv("POSTGRES_DB", "instagram_dm_sender"),
    "USER": getenv("POSTGRES_USER", "arka"),
    "PASSWORD": getenv("POSTGRES_PASSWORD", "arka"),
    "HOST": getenv("POSTGRES_HOST", "localhost"),
    "PORT": int(getenv("POSTGRES_PORT", "5435")),
    "CONN_MAX_AGE": 60,
}
db_settings = DB

if is_testing():
    db_settings = TEST_DB

DATABASES = {
    "default": DB,  # FIXME
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": (
            getenv("REDIS_DEFAULT_CACHE", "redis://localhost:6379/0")
            if not Mode.test
            else "redis://localhost:6379/15"
        ),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 100,
                "retry_on_timeout": True,
            },
            "SENTINEL_KWARGS": {
                "socket_timeout": 0.1,
            },
        },
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
