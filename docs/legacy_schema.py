# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountTemplate(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey('Accounts', models.DO_NOTHING)
    template = models.ForeignKey('Templates', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_template'


class Accounts(models.Model):
    id = models.BigAutoField(primary_key=True)
    secret_key = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(unique=True, max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_pic_url = models.TextField(blank=True, null=True)
    instagram_state = models.CharField(max_length=255)
    app_state = models.CharField(max_length=255)
    color = models.ForeignKey('Colors', models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey('Categories', models.DO_NOTHING, blank=True, null=True)
    proxy = models.ForeignKey('Proxies', models.DO_NOTHING, blank=True, null=True)
    profile = models.ForeignKey('Profiles', models.DO_NOTHING, blank=True, null=True)
    is_used = models.SmallIntegerField()
    avatar_changed = models.SmallIntegerField()
    username_changed = models.SmallIntegerField()
    initial_posts_deleted = models.SmallIntegerField()
    has_enough_posts = models.SmallIntegerField()
    is_public = models.SmallIntegerField()
    is_active = models.SmallIntegerField()
    web_session = models.TextField(blank=True, null=True)
    mobile_session = models.TextField(blank=True, null=True)
    log = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    next_login = models.DateTimeField(blank=True, null=True)
    fingerprint = models.JSONField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True)
    screenshot_taken = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'accounts'


class AdsPowerLocks(models.Model):
    last_executed_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ads_power_locks'


class Cache(models.Model):
    key = models.CharField(primary_key=True, max_length=255)
    value = models.TextField()
    expiration = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cache'


class CacheLocks(models.Model):
    key = models.CharField(primary_key=True, max_length=255)
    owner = models.CharField(max_length=255)
    expiration = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cache_locks'


class Categories(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    number_of_follow_ups = models.IntegerField()
    hour_interval = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'


class Clis(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Accounts, models.DO_NOTHING)
    process = models.ForeignKey('Processes', models.DO_NOTHING, blank=True, null=True)
    log = models.CharField(max_length=255)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'clis'


class Colors(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=255)
    is_used = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'colors'


class Commands(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Accounts, models.DO_NOTHING, blank=True, null=True)
    lead = models.ForeignKey('Leads', models.DO_NOTHING, blank=True, null=True)
    parent_command = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    commandable_id = models.IntegerField(blank=True, null=True)
    commandable_type = models.CharField(max_length=255, blank=True, null=True)
    times = models.IntegerField()
    type = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commands'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DmPostLead(models.Model):
    id = models.BigAutoField(primary_key=True)
    lead = models.ForeignKey('Leads', models.DO_NOTHING)
    dm_post = models.ForeignKey('DmPosts', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dm_post_lead'
        unique_together = (('dm_post', 'lead'),)


class DmPosts(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    priority = models.SmallIntegerField(blank=True, null=True)
    media_id = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dm_posts'


class Hashtags(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=255)
    is_used = models.SmallIntegerField()
    category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hashtags'


class LeadHistories(models.Model):
    id = models.BigAutoField(primary_key=True)
    state = models.CharField(max_length=255)
    times = models.IntegerField(blank=True, null=True)
    lead = models.ForeignKey('Leads', models.DO_NOTHING)
    account = models.ForeignKey(Accounts, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'lead_histories'


class LeadSources(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=255)
    is_used = models.SmallIntegerField()
    category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lead_sources'


class Leads(models.Model):
    id = models.BigAutoField(primary_key=True)
    instagram_id = models.BigIntegerField(blank=True, null=True)
    username = models.CharField(unique=True, max_length=255)
    times = models.IntegerField(blank=True, null=True)
    last_state = models.CharField(max_length=255)
    account = models.ForeignKey(Accounts, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    export_date = models.DateTimeField(blank=True, null=True, db_comment='Date we pull lead')
    last_command_send_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'leads'


class Logs(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Accounts, models.DO_NOTHING)
    log = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'logs'


class Looms(models.Model):
    id = models.BigAutoField(primary_key=True)
    hashed_name = models.CharField(max_length=255)
    original_name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=255)
    account = models.ForeignKey(Accounts, models.DO_NOTHING, blank=True, null=True)
    lead = models.ForeignKey(Leads, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'looms'


class Messages(models.Model):
    id = models.BigAutoField(primary_key=True)
    message_id = models.CharField(max_length=255, blank=True, null=True)
    thread = models.ForeignKey('Threads', models.DO_NOTHING, blank=True, null=True)
    messageable_id = models.BigIntegerField(blank=True, null=True)
    messageable_type = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    sender = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'messages'


class Migrations(models.Model):
    migration = models.CharField(max_length=255)
    batch = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


class Notifs(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Accounts, models.DO_NOTHING)
    lead = models.ForeignKey(Leads, models.DO_NOTHING)
    thread = models.ForeignKey('Threads', models.DO_NOTHING)
    message = models.ForeignKey(Messages, models.DO_NOTHING)
    visibility = models.CharField(max_length=255)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'notifs'


class PermissionRole(models.Model):
    permission = models.OneToOneField('Permissions', models.DO_NOTHING, primary_key=True)  # The composite primary key (permission_id, role_id) found, that is not supported. The first column is selected.
    role = models.ForeignKey('Roles', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'permission_role'
        unique_together = (('permission', 'role'),)


class PermissionUser(models.Model):
    permission = models.ForeignKey('Permissions', models.DO_NOTHING)
    user_id = models.BigIntegerField(primary_key=True)  # The composite primary key (user_id, permission_id, user_type) found, that is not supported. The first column is selected.
    user_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'permission_user'
        unique_together = (('user_id', 'permission', 'user_type'),)


class Permissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permissions'


class PersonalAccessTokens(models.Model):
    id = models.BigAutoField(primary_key=True)
    tokenable_type = models.CharField(max_length=255)
    tokenable_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    token = models.CharField(unique=True, max_length=64)
    abilities = models.TextField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personal_access_tokens'


class Processes(models.Model):
    id = models.BigAutoField(primary_key=True)
    pid = models.BigIntegerField(unique=True)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'processes'


class Profiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    folder = models.CharField(max_length=255)
    profile_id = models.CharField(max_length=255)
    proxy = models.ForeignKey('Proxies', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    is_used = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'profiles'


class Proxies(models.Model):
    id = models.BigAutoField(primary_key=True)
    ip = models.CharField(max_length=255)
    port = models.IntegerField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    is_used = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'proxies'


class RoleUser(models.Model):
    role = models.ForeignKey('Roles', models.DO_NOTHING)
    user_id = models.BigIntegerField(primary_key=True)  # The composite primary key (user_id, role_id, user_type) found, that is not supported. The first column is selected.
    user_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'role_user'
        unique_together = (('user_id', 'role', 'user_type'),)


class Roles(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class ScreenResolutions(models.Model):
    id = models.BigAutoField(primary_key=True)
    width = models.IntegerField()
    height = models.IntegerField()
    is_used = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'screen_resolutions'


class ScreenShots(models.Model):
    id = models.BigAutoField(primary_key=True)
    cause = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    account = models.ForeignKey(Accounts, models.DO_NOTHING)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'screen_shots'


class Sessions(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    user_id = models.BigIntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    payload = models.TextField()
    last_activity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sessions'


class Settings(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, null=True)
    key = models.CharField(max_length=255)
    value = models.TextField()
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'settings'


class Spintaxes(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    times = models.IntegerField()
    text = models.TextField()
    category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spintaxes'


class Taggables(models.Model):
    tag = models.ForeignKey('Tags', models.DO_NOTHING)
    taggable_id = models.IntegerField()
    taggable_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'taggables'


class Tags(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tags'


class Templates(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField()
    caption = models.TextField(blank=True, null=True)
    carousel_id = models.CharField(max_length=255, blank=True, null=True)
    uid = models.CharField(max_length=255, blank=True, null=True)
    color = models.ForeignKey(Colors, models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    type = models.CharField(max_length=255)
    sub_type = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'templates'


class Threads(models.Model):
    id = models.BigAutoField(primary_key=True)
    thread_id = models.CharField(max_length=255, blank=True, null=True)
    thread_url_id = models.CharField(max_length=255, blank=True, null=True)
    account = models.ForeignKey(Accounts, models.DO_NOTHING, blank=True, null=True)
    lead = models.ForeignKey(Leads, models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'threads'
        unique_together = (('account', 'lead'),)


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Warnings(models.Model):
    id = models.BigAutoField(primary_key=True)
    cause = models.TextField(blank=True, null=True)
    duration = models.IntegerField()
    account = models.ForeignKey(Accounts, models.DO_NOTHING)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'warnings'
