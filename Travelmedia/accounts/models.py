from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from Travelmedia.accounts.managers import AccountUserManager
from django.utils import timezone
class AccountUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    USERNAME_FIELD = "email"

    objects = AccountUserManager()




class Profile(models.Model):
    MAX_FIRST_NAME_LENGTH = 30
    MAX_LAST_NAME_LENGTH = 30



    first_name = models.CharField(
        max_length=MAX_FIRST_NAME_LENGTH,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        max_length=MAX_LAST_NAME_LENGTH,
        blank=True,
        null=True,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    profile_picture = models.URLField(
        blank=True,
        null=True,
    )

    user = models.OneToOneField(
        AccountUser,
        on_delete=models.CASCADE,
    )

    def calculate_age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - (
                        (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            return age
        return None
