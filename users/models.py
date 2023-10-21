import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    class Meta:
        indexes = [
            models.Index(fields=["uuid"], name="user_uuid_idx"),
        ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = None  # type: ignore[assignment]
    email = models.EmailField(_("email address"), unique=True)
    mobile_number = models.CharField(max_length=13, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_mobile_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()  # type: ignore[misc, assignment]

    def __str__(self) -> str:
        return self.email


class Profile(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["uuid"], name="profile_uuid_idx"),
        ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, to_field="uuid", on_delete=models.CASCADE)
