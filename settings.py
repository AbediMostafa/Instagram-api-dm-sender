from os import getenv


class TestAccountData:
    username = getenv("MASSDM_TEST_ACCOUNT_USERNAME", "choob_lab_style")
    password = getenv("MASSDM_TEST_ACCOUNT_PASSWORD", "i39vflh7dmsfldf25")
    secret = getenv("MASSDM_TEST_ACCOUNT_SECRET", "6exvtnvolefjwqq7etlkjuh25qle2bv7")


class Mode:
    test = "TEST"
    debug = "DEBUG"
    production = "PRO"


class General:
    proxy = getenv(
        "MASSDM_PROXY", "http://germanproxy42de:HxxDt7rfpwWn@x462.fxdx.in:13916"
    )
    runtime_mode = getenv("MASSDM_RUNITME_MODE", Mode.test)


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
