from django.contrib.auth.models import AbstractUser
from django.db import models

from graintrack_store.core.models import BaseModel
from graintrack_store.users.constants import UserConstants


class User(BaseModel, AbstractUser):
    role = models.CharField(
        choices=UserConstants.USER_ROLES,
        default=UserConstants.USER_ROLES.DEFAULT,
        max_length=UserConstants.USER_ROLES_MAX_LENGTH,
    )

    class Meta:
        db_table = "users"
