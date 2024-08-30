from django.contrib.auth.models import AbstractUser
from django.db import models

from graintrack_store.core.models import BaseModel
from graintrack_store.users.constants import UserConstants


class User(BaseModel, AbstractUser):
    role = models.CharField(
        choices=UserConstants.ROLE_CHOICE,
        default=UserConstants.ROLE_CHOICE.DEFAULT,
        max_length=UserConstants.ROLE_MAX_LENGTH,
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"
