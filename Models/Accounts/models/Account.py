from typing import override

from django.db import models
from okane.BaseModel import BaseModel
from Models.Users.models.User import User


class Account(BaseModel):
    name: models.CharField[str | None, str] = models.CharField(max_length=20)
    owner: models.ForeignKey[User, User] = models.ForeignKey(User, on_delete=models.CASCADE)

    @override
    def __str__(self):
        return self.name
    