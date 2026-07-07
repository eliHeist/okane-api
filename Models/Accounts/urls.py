from django.urls import path
from ninja import NinjaAPI
from .api import router

app_name = "Accounts"

# Create a separate API instance for accounts
accounts_api = NinjaAPI(urls_namespace="accounts_api")
accounts_api.add_router("accounts/", router)

urlpatterns = [
    path("api/", accounts_api.urls),
]