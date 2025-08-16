from datetime import datetime, timezone
from typing import Self
from tortoise import fields, models


class Account(models.Model):
    proxy = fields.BigIntField(null=True)
    color = fields.BigIntField(null=True)
    screen_resolution = fields.BigIntField(null=True)
    profile = fields.BigIntField(null=True)

    category = fields.BigIntField(null=True)
    secret_key = fields.CharField(max_length=255, null=True)
    username = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255, null=True)
    bio = fields.TextField(null=True)
    email = fields.TextField(null=True)
    profile_pic_url = fields.TextField(null=True)
    instagram_state = fields.CharField(max_length=50, default="active")
    app_state = fields.CharField(max_length=50, default="idle")
    avatar_changed = fields.SmallIntField(default=0)
    username_changed = fields.SmallIntField(default=0)
    initial_posts_deleted = fields.SmallIntField(default=0)
    has_enough_posts = fields.SmallIntField(default=0)
    is_used = fields.SmallIntField(default=0)
    is_active = fields.SmallIntField(default=1)
    is_public = fields.SmallIntField(default=0)
    web_session = fields.TextField(null=True)
    mobile_session = fields.TextField(null=True)
    log = fields.TextField(null=True)
    updated_at = fields.DatetimeField(null=True)  # TODO: add timezone
    next_login = fields.DatetimeField(null=True)

    class Meta:
        table = "accounts"

    @classmethod
    async def pick_ready_ones(cls) -> list[Self]:
        """
        This is the logic for selection of accounts that are ready to work at the moment
        """
        return await cls.filter(next_login__lt=datetime.now(), is_used=0)


class User(models.Model):
    username = fields.CharField(max_length=256)
    password = fields.CharField(max_length=256)

    class Meta:
        table = "users"


class Category(models.Model):
    title = fields.CharField(max_length=256)
    description = fields.TextField(null=True)
    number_of_follow_ups = fields.IntField(default=0)
    hour_interval = fields.IntField(default=24)  # New field added
    updated_at = fields.DatetimeField(null=True, auto_now=True)

    class Meta:
        table = "categories"


class Spintax(models.Model):
    name = fields.CharField(max_length=256)
    times = fields.IntField()
    text = fields.TextField()
    category = fields.ForeignKeyField(
        "models.Category", related_name="commands", null=True
    )
    user_id = fields.ForeignKeyField("models.User")
    updated_at = fields.DatetimeField(null=True)

    @classmethod
    def get_value(cls, times, category=None, default=None):
        query = cls.filter(times=times)
        if category is not None:
            query = query.filter(category=category)

        record = query.first()
        return record.text if record else default

    class Meta:
        table = "spintaxes"


class Lead(models.Model):
    username = fields.CharField(max_length=255)
    instagram_id = fields.BigIntField(null=True)
    times = fields.IntField(default=0)
    last_state = fields.CharField(max_length=255, default="free")
    account = fields.ForeignKeyField("models.Account", backref="leads", null=True)
    category = fields.ForeignKeyField("models.Category", related_name="leads", null=True)

    last_command_send_date = fields.DatetimeField(null=True)

    class Meta:
        table = "leads"


class DmPost(models.Model):
    title = fields.CharField(max_length=255)
    category = fields.ForeignKeyField(
        "models.Category", related_name="lead_sources", null=True
    )
    description = fields.TextField(null=True)
    # times :turn of message
    times = fields.IntField(default=0)

    class Meta:
        table_name = "dm_posts"
