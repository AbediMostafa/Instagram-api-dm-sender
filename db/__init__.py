# from db.base import init
# from db.models import Account, Category, User, Spintax, Lead, DmPost

# __all__ = ["Account", "init", "Category", "User", "Spintax", "Lead", "DmPost"]
def setup_django():
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    django.setup()

