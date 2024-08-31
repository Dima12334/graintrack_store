from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
