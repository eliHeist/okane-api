from ninja import Router
from ninja import Schema
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from asgiref.sync import sync_to_async

from typing import Optional

router = Router()
User = get_user_model()





