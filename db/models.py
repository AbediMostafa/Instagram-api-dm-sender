from django.db import models
from django.db.models import OuterRef, Subquery
from django.db.transaction import atomic
from django.utils.timezone import now
import spintax
from django.utils.translation import gettext_lazy as _
from django.forms.models import model_to_dict


class Account(models.Model):
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
    color = models.ForeignKey("db.Color", models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(
        "db.Category", models.DO_NOTHING, blank=True, null=True
    )
    proxy = models.ForeignKey("db.Proxy", models.SET_NULL, blank=True, null=True)
    profile = models.ForeignKey("db.Profile", models.DO_NOTHING, blank=True, null=True)
    is_used = models.SmallIntegerField()
    used_at = models.DateTimeField(null=True, blank=True)
    avatar_changed = models.SmallIntegerField()
    username_changed = models.SmallIntegerField()
    initial_posts_deleted = models.SmallIntegerField()
    has_enough_posts = models.SmallIntegerField()
    is_public = models.SmallIntegerField(choices=[(0, 0), (1, 1)])
    is_active = models.SmallIntegerField(choices=[(0, 0), (1, 1)])
    web_session = models.TextField(blank=True, null=True)
    mobile_session = models.TextField(blank=True, null=True)
    log = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    next_login = models.DateTimeField(blank=True, null=True)
    fingerprint = models.JSONField(blank=True, null=True)
    phone = models.CharField(max_length=31, blank=True, null=True)
    screenshot_taken = models.SmallIntegerField()
    user = models.ForeignKey("db.User", on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = "accounts"

    def to_dict(self):
        return model_to_dict(self)

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "users"


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    number_of_follow_ups = models.IntegerField()
    hour_interval = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "categories"


class LeadState(models.TextChoices):
    FREE = "fr", "Free"
    FOLLOWED = (
        "fl",
        "Followed",
    )  # can an account be free and followed at the same time?!
    PENDING = "p", "Pending"


class LeadQuerySet(models.QuerySet):
    def build_messages(self) -> models.QuerySet["Lead"]:
        """
        Gets the Lead records annotated with the messages that should be deliver to them
        """
        leads = Lead.objects.filter(state=LeadState.FREE)
        leads = leads.annotate(
            dm_post_id=Subquery(
                DmPost.objects.filter(priority=OuterRef("times") + 1).values("id")[:1]
            )
        )
        return leads

    @atomic()
    def select_for_send(self):
        self.select_for_update()
        self.update(state=LeadState.PENDING)
        return True


class Lead(models.Model):
    objects: models.Manager["Lead"] = LeadQuerySet.as_manager()

    id = models.BigAutoField(primary_key=True)
    instagram_id = models.BigIntegerField(blank=True, null=True)
    username = models.CharField(unique=True, max_length=255)
    times = models.IntegerField(blank=True, null=True)
    state = models.CharField(
        max_length=255,
        choices=LeadState.choices,
        db_column="last_state",
        default=LeadState.FREE,
    )
    account = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    export_date = models.DateTimeField(
        blank=True, null=True, db_comment="Date we pull lead"
    )
    last_command_send_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "leads"


class DmPostLead(models.Model):
    id = models.BigAutoField(primary_key=True)
    lead = models.ForeignKey(Lead, models.DO_NOTHING)
    dm_post = models.ForeignKey("db.DmPost", models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        db_table = "dm_post_lead"
        unique_together = (("dm_post", "lead"),)


class DmPost(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    priority = models.SmallIntegerField(blank=True, null=True)
    media_id = models.CharField(unique=True, max_length=255, blank=True, null=True)
    leads = models.ManyToManyField("db.Lead", through="db.DmPostLead")
    spintax = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "dm_posts"

    @property
    def text(self) -> str:
        return spintax.spin(self.spintax)


class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    folder = models.CharField(max_length=255)
    profile_id = models.CharField(max_length=255)
    proxy = models.ForeignKey("db.Proxy", models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    is_used = models.SmallIntegerField()

    class Meta:
        db_table = "profiles"


class Proxy(models.Model):
    id = models.BigAutoField(primary_key=True)
    ip = models.CharField(max_length=255)
    port = models.IntegerField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    is_used = models.SmallIntegerField()

    class Meta:
        db_table = "proxies"


class Color(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=255)
    is_used = models.SmallIntegerField()

    class Meta:
        db_table = "colors"
