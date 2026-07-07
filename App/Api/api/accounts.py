from django.http import HttpRequest
from ninja import Router
from uuid import UUID

from Models.Accounts.models import Account
from Models.Accounts.schemas import AccountCreate, AccountUpdate, AccountRead

router = Router()


@router.get("/", response=list[AccountRead], url_name="list_accounts")
def list_accounts(request: HttpRequest):
    """List all accounts"""
    return Account.objects.all()


@router.get("/{account_id}", response=AccountRead, url_name="get_account")
def get_account(request: HttpRequest, account_id: UUID):
    """Get a specific account by ID"""
    try:
        return Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        return {"error": "Account not found"}, 404


@router.post("/", response=AccountRead, url_name="create_account")
def create_account(request: HttpRequest, payload: AccountCreate):
    """Create a new account"""
    account = Account.objects.create(**payload.dict())
    return account


@router.put("/{account_id}", response=AccountRead, url_name="update_account")
def update_account(request: HttpRequest, account_id: UUID, payload: AccountUpdate):
    """Update an account"""
    try:
        account = Account.objects.get(id=account_id)
        update_data = payload.dict(exclude_unset=True)
        for attr, value in update_data.items():
            setattr(account, attr, value)
        account.save()
        return account
    except Account.DoesNotExist:
        return {"error": "Account not found"}, 404


@router.patch("/{account_id}", response=AccountRead, url_name="partial_update_account")
def partial_update_account(request: HttpRequest, account_id: UUID, payload: AccountUpdate):
    """Partially update an account"""
    try:
        account = Account.objects.get(id=account_id)
        update_data = payload.dict(exclude_unset=True)
        for attr, value in update_data.items():
            if value is not None:
                setattr(account, attr, value)
        account.save()
        return account
    except Account.DoesNotExist:
        return {"error": "Account not found"}, 404


@router.delete("/{account_id}", url_name="delete_account")
def delete_account(request: HttpRequest, account_id: UUID):
    """Delete an account"""
    try:
        account = Account.objects.get(id=account_id)
        account.delete()
        return {"message": "Account deleted successfully"}
    except Account.DoesNotExist:
        return {"error": "Account not found"}, 404
