from ninja import Schema
from uuid import UUID
from datetime import datetime


class AccountCreate(Schema):
    """Schema for creating an Account"""
    name: str


class AccountUpdate(Schema):
    """Schema for updating an Account"""
    name: str


class AccountRead(Schema):
    """Schema for reading an Account"""
    id: UUID
    name: str
    created: datetime
