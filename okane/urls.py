from django.contrib import admin
from django.urls import path, include

from App.Api.api.base import api

from .appsConfig import getAppUrls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

urlpatterns += getAppUrls()