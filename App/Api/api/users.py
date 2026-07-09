from ninja import Router
from django.http import HttpRequest
from django.contrib.auth import aauthenticate, alogin, alogout, aget_user, get_user_model
from asgiref.sync import sync_to_async
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError



from Models.Users.schemas import (
    UserCreate, UserRead, UserUpdate,
    LoginSchema, ChangePasswordSchema,
)
from Models.Users.schemas.UserSchema import PasswordResetConfirmSchema, PasswordResetRequestSchema, PasswordResetValidateSchema

router = Router()
User = get_user_model()


@router.post("/register", response=UserRead)
async def register(request: HttpRequest, payload: UserCreate) -> User:
    """Register a new user (async)"""
    user = await User.objects.acreate(
        email=payload.email,
        password=payload.password,
        first_name=payload.first_name,
        last_name=payload.last_name,
        username=payload.username,
    )
    return user


@router.post("/login", response=UserRead)
async def login(request: HttpRequest, payload: LoginSchema) -> User | tuple[dict[str, str], int]:
    """Authenticate and login a user (async)"""
    user = await aauthenticate(request=request, email=payload.email, password=payload.password)
    if not user:
        return {"error": "Invalid credentials"}, 401

    # create session
    await alogin(request, user)
    return user


@router.post("/logout")
async def logout(request: HttpRequest):
    """Logout the current user (async)"""
    await alogout(request)
    return {"message": "Logged out"}


@router.get("/me", response=UserRead)
async def me(request: HttpRequest):
    """Get current authenticated user (async)"""
    user = await aget_user(request)
    if not user or user.is_anonymous:
        return {"error": "Not authenticated"}, 401
    return user


@sync_to_async
def get_user_by_email_or_username(email: str | None, username: str | None) -> User | None:
    try:
        if email:
            return User.objects.get(email=email)
        if username:
            return User.objects.get(username=username)
        return None
    except User.DoesNotExist:
        return None

@sync_to_async
def get_user_by_uidb64(uidb64: str):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        return User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None

@sync_to_async
def check_token(user: User, token: str) -> bool:
    return default_token_generator.check_token(user, token)

@sync_to_async
def reset_user_password(user: User, new_password: str):
    # This triggers both standard hashing and validation checks
    validate_password(new_password, user)
    user.set_password(new_password)
    user.save()


# --- 1. REQUEST ENDPOINT ---
@router.post("/password-reset/request", response={200: dict})
async def password_reset_request(request, data: PasswordResetRequestSchema):
    user = await get_user_by_email_or_username(data.email, data.username)
    
    if user:
        # Generate the safe base64 UID and one-time token
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        # TODO: Construct your frontend URL and trigger an email dispatch
        # example_url = f"https://okane.app/reset-password?uid={uidb64}&token={token}"
        # await send_reset_email(user.email, example_url)
        print(f"Generated Token for {user.email}: uid={uidb64}, token={token}")

    # Always return a 200 success response to avoid user harvesting
    return {"detail": "If your email matches an active account, password reset instructions have been sent."}


# --- 2. VALIDATION ENDPOINT ---
@router.post("/password-reset/validate", response={200: dict, 400: dict})
async def password_reset_validate(request, data: PasswordResetValidateSchema):
    user = await get_user_by_uidb64(data.uidb64)
    
    if user and await check_token(user, data.token):
        return {"detail": "Token is valid."}
        
    return 400, {"error": "Invalid or expired reset token."}


# --- 3. CONFIRMATION ENDPOINT ---
@router.post("/password-reset/confirm", response={200: dict, 400: dict})
async def password_reset_confirm(request, data: PasswordResetConfirmSchema):
    user = await get_user_by_uidb64(data.uidb64)
    
    if not user or not await check_token(user, data.token):
        return 400, {"error": "Invalid or expired reset token."}
        
    try:
        # Validate, hash, and commit the new password to the database
        await reset_user_password(user, data.new_password)
        return {"detail": "Password has been updated successfully."}
    except ValidationError as e:
        return 400, {"error": e.messages}
