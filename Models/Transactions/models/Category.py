from typing import override

from django.db import models
from okane.BaseModel import BaseModel

class Category(BaseModel):
    name: models.CharField[str | None, str] = models.CharField(max_length=20)

    @override
    def __str__(self):
        return self.name
    