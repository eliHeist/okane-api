from decimal import Decimal
from typing import override
from django.db import models
from okane.BaseModel import BaseModel

from Models.Accounts.models.Account import Account
from Models.Transactions.models.Category import Category
from Models.Transactions.models.Transaction import Transaction


class JournalEntry(BaseModel):
    """
    The Line Items.
    This links your Accounts, Categories, and Amounts together.
    """
    transaction: models.ForeignKey[Transaction, Transaction] = models.ForeignKey(
        Transaction, 
        on_delete=models.CASCADE, 
        related_name='entries'
    )
    
    # An entry can affect an Account, a Category, or BOTH (depending on the type)
    account: models.ForeignKey[Account, Account] = models.ForeignKey(Account, on_delete=models.PROTECT)
    category: models.ForeignKey[Category, Category] = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    
    # Use positive for money coming in, negative for money going out
    amount: models.DecimalField[Decimal, Decimal] = models.DecimalField(max_digits=12, decimal_places=2)

    @override
    def __str__(self):
        return str(self.amount)
