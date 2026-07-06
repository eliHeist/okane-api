import uuid
from django.db import models

from Models.Accounts.models.Account import Account
from Models.Transactions.models.Category import Category
from Models.Transactions.models.Transaction import Transaction


class JournalEntry(models.Model):
    """
    The Line Items.
    This links your Accounts, Categories, and Amounts together.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(
        Transaction, 
        on_delete=models.CASCADE, 
        related_name='entries'
    )
    
    # An entry can affect an Account, a Category, or BOTH (depending on the type)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    
    # Use positive for money coming in, negative for money going out
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.amount
