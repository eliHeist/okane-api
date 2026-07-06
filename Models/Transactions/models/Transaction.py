import uuid
from django.db import models


class TransactionTypes(models.TextChoices):
    INCOME = '+', _('Income')
    EXPENSE = '-', _('Expense')
    TRANSFER = '=', _('Transfer')


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    posted_at = models.DateTimeField(db_index=True)
    description = models.CharField(max_length=255)
    type = models.CharField(
            max_length=1, 
            choices=TransactionTypes.choices,
            default=TransactionTypes.EXPENSE
        )
    
    created = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.description} ({self.get_type_display()})"

