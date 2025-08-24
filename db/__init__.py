import sys


def setup_django():
    import django
    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    django.setup()


try:
    setup_django()
except RuntimeError as e:
    if "populate() isn't reentrant" in str(e):
        pass  # Django is already populating, ignore
    else:
        raise
