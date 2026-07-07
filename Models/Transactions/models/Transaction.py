from datetime import datetime
from typing import override
from okane.BaseModel import BaseModel
from django.db import models

from django.utils.translation import gettext_lazy as _


TransactionTypes = models.TextChoices('TransactionTypes', [
    ('INCOME', ('+', _('Income'))),
    ('EXPENSE', ('-', _('Expense'))),
    ('TRANSFER', ('=', _('Transfer'))),
])


class Transaction(BaseModel):
    posted_at: models.DateTimeField[datetime, datetime] = models.DateTimeField(db_index=True)
    description: models.CharField[str, str] = models.CharField(max_length=255)
    type: models.CharField[str, str] = models.CharField(
            max_length=1, 
            choices=TransactionTypes.choices,
            default=TransactionTypes.EXPENSE
        )

    @override
    def __str__(self):
        return f"{self.type} {self.description}"

