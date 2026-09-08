"""Standalone URL mounting for admin and the shared runtime."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("education_runtime.urls")),
]
