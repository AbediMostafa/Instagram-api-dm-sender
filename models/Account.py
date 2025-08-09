from peewee import *

from dotenv import load_dotenv

from .Base import BaseModel


class Account(BaseModel):
    proxy = BigIntegerField()
    color = BigIntegerField()
    screen_resolution = BigIntegerField()
    profile = BigIntegerField()
    category = BigIntegerField()

    secret_key = CharField(null=True)
    username = CharField()
    password = CharField()
    name = CharField(null=True)
    bio = TextField(null=True)
    email = TextField(null=True)
    profile_pic_url = TextField(null=True)
    instagram_state = CharField(default='active')
    app_state = CharField(default='idle')
    avatar_changed = SmallIntegerField(default=0)
    username_changed = SmallIntegerField(default=0)
    initial_posts_deleted = SmallIntegerField(default=0)
    has_enough_posts = SmallIntegerField(default=0)
    is_used = SmallIntegerField(default=0)
    is_active = SmallIntegerField(default=1)
    is_public = SmallIntegerField(default=0)
    web_session = TextField(null=True)
    mobile_session = TextField(null=True)
    log = TextField(null=True)
    updated_at = DateTimeField(null=True)
    next_login = DateTimeField(null=True)

    # Possibilities
    passed_days_since_creation = None
    allowed_number_of_dms = None
    allowed_number_of_dm_follow_ups = None
    allowed_number_of_loom_follow_ups = None
    todays_sent_dms = None
    final_allowed_number_of_dms = None

    can_send_dm_today = None
    can_send_dm_follow_up_today = None
    can_send_loom_follow_up_today = None
    number_of_custom_message_commands = None
    custom_message_commands = None
    current_chunk_dm = None

    class Meta:
        table_name = 'accounts'
from models.Base import database as db

if __name__ == '__main__':
    # db.connect()
    Account.filter()
    d=db.create_tables([Account])
    db.close()
    
    
