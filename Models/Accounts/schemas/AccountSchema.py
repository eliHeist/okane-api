from ninja import Schema
from uuid import UUID
from datetime import datetime


class AccountCreate(BaseModel):
    """Schema for creating an Account"""
    name: str


class AccountUpdate(BaseModel):
    """Schema for updating an Account"""
    name: str


class AccountRead(BaseModel):
    """Schema for reading an Account"""
    id: UUID
    name: str
    created: datetime
