from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    