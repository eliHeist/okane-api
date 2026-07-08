from django.urls import path
from ninja import NinjaAPI
from .api import router

app_name = "Users"

users_api = NinjaAPI(urls_namespace="users_api")
users_api.add_router("auth/", router)

urlpatterns = [
    path("api/", users_api.urls),
]