from ninja import Schema
from uuid import UUID
from datetime import datetime
from typing import Literal

from Models.Transactions.schemas.JournalEntrySchema import JournalEntryReadFull


class TransactionCreate(Schema):
    """Schema for creating a Transaction"""
    posted_at: datetime
    description: str
    type: Literal['+', '-', '=']


class TransactionUpdate(Schema):
    """Schema for updating a Transaction"""
    posted_at: datetime
    description: str
    type: Literal['+', '-', '=']


class TransactionRead(Schema):
    """Schema for reading a Transaction"""
    id: UUID
    posted_at: datetime
    description: str
    type: Literal['+', '-', '=']
    created: datetime


class TransactionReadWithJournals(Schema):
    """Schema for reading a Transaction with its JournalEntry"""
    id: UUID
    posted_at: datetime
    description: str
    type: Literal['+', '-', '=']
    created: datetime
    journal: list[JournalEntryReadFull]
