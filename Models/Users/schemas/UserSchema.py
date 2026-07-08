from pydantic import EmailStr
from ninja import Schema
from datetime import datetime


class UserCreate(Schema):
    """Schema for creating a User"""
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None


class UserUpdate(Schema):
    """Schema for updating a User"""
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None


class UserRead(Schema):
    """Schema for reading a User"""
    id: int
    email: str
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class LoginSchema(Schema):
    email: EmailStr
    password: str


class PasswordResetRequestSchema(Schema):
    email: EmailStr | None
    username: str | None

class PasswordResetValidateSchema(Schema):
    uidb64: str
    token: str

class PasswordResetConfirmSchema(Schema):
    uidb64: str
    token: str
    new_password: str
