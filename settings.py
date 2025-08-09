from os import getenv


class TestAccountData:
    username = getenv("MASSDM_TEST_ACCOUNT_USERNAME", "choob_lab_style")
    password = getenv("MASSDM_TEST_ACCOUNT_PASSWORD", "i39vflh7dmsfldf25")
    secret = getenv("MASSDM_TEST_ACCOUNT_SECRET", "6exvtnvolefjwqq7etlkjuh25qle2bv7")


class General:
    PROXY = getenv(
        "MASSDM_PROXY", "http://germanproxy42de:HxxDt7rfpwWn@x462.fxdx.in:13916"
    )