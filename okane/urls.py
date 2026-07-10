# from django.conf import settings
# from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from App.Api.api.base import api

from okane.registry import app_urls

app_urls.discover('App.Client.views')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

urlpatterns += app_urls.patterns

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)