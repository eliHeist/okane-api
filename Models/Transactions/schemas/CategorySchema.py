from ninja import Schema
from uuid import UUID


class CategoryCreate(Schema):
    """Schema for creating a Category"""
    name: str


class CategoryUpdate(Schema):
    """Schema for updating a Category"""
    name: str


class CategoryRead(Schema):
    """Schema for reading a Category"""
    id: UUID
    name: str
