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
    updated_at = fields.DatetimeField(null=True)
    next_login = fields.DatetimeField(null=True)

    class Meta:
        table = "accounts"

    @classmethod
    async def pick_ready_ones(cls) -> list[Self]:
        """
        This is the logic for selection of accounts that are ready to work at the moment
        """
        return await cls.filter(next_login__lt=datetime.now(), is_used=0)
