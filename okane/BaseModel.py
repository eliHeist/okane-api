import datetime
import uuid
from django.db import models

class BaseModel(models.Model):
    id: models.UUIDField[uuid.UUID | str, uuid.UUID] = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at: models.DateTimeField[datetime.datetime | None, datetime.datetime] = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField[datetime.datetime | None, datetime.datetime] = models.DateTimeField(auto_now=True)

    class Meta:
        abstract: bool = True
