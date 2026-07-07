from ninja import Schema
from uuid import UUID
from decimal import Decimal

from Models.Accounts.schemas.AccountSchema import AccountRead
from Models.Transactions.schemas.CategorySchema import CategoryRead


class JournalEntryCreate(Schema):
    """Schema for creating a JournalEntry"""
    transaction: UUID
    account: UUID
    category: UUID | None = None
    amount: Decimal


class JournalEntryUpdate(Schema):
    """Schema for updating a JournalEntry"""
    transaction: UUID
    account: UUID
    category: UUID | None = None
    amount: Decimal


class JournalEntryRead(Schema):
    """Schema for reading a JournalEntry"""
    id: UUID
    transaction: UUID
    account: UUID
    category: UUID | None = None
    amount: Decimal

class JournalEntryReadFull(Schema):
    """Schema for reading a JournalEntry"""
    id: UUID
    account: AccountRead
    category: CategoryRead | None
    amount: Decimal
