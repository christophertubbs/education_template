"""Root URL configuration for the generated standalone host."""

from __future__ import annotations

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


urlpatterns = [
    path("", lambda request: redirect("__APP_NAME__:index")),
    path("admin/", admin.site.urls),
    path("__REPOSITORY_NAME__/", include("__APP_NAME__.urls")),
]
