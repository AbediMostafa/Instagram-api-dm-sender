from tortoise import Tortoise, models


async def init(*, migrate_schema=False, **kwargs):
    config = {
        "connections": {
            "default": {
                "engine": "tortoise.backends.asyncpg",
                "credentials": {
                    "host": kwargs["host"],
                    "port": kwargs["port"],
                    "user": kwargs["user"],
                    "password": kwargs["password"],
                    "database": kwargs["database"],
                    "min_size": kwargs["min_connections"],
                    "max_size": kwargs["max_connections"], 
                },
            }
        },
        "apps": {
            "models": {
                "models": ["models"],  # or your app's models module
                "default_connection": "default",
            }
        },
        'timezone': 'Asia/Tehran'
    }

    await Tortoise.init(config=config)
    if migrate_schema:
        await Tortoise.generate_schemas()


class BaseModel(models.Model):
    pass

    class Meta:
        abstract = True
