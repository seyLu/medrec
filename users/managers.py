from typing import Any

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager[AbstractUser]):
    """
    User model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(
        self, email: str, password: str, **extra_fields: dict[str, Any]
    ) -> Any:
        """
        Create and save a user with the given email and password.
        """

        if not email:
            raise ValueError(_("The Email must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, email: str, password: str, **extra_fields: dict[str, Any]
    ) -> Any:
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault("is_active", True)  # type: ignore[arg-type]
        extra_fields.setdefault("is_staff", True)  # type: ignore[arg-type]
        extra_fields.setdefault("is_superuser", True)  # type: ignore[arg-type]

        if extra_fields.get("is_staff") is not True:  # type: ignore[comparison-overlap]
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:  # type: ignore[comparison-overlap]
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)
