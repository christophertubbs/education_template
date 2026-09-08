"""URL routes for the generated curriculum application."""

from __future__ import annotations

from django.urls import path

from . import views


app_name = "__APP_NAME__"

urlpatterns = [
    path("", views.index, name="index"),
    path("lessons/<slug:identifier>/", views.lesson_detail, name="lesson"),
    path("assessments/<slug:identifier>/", views.assessment_detail, name="assessment"),
    path("glossary/", views.glossary, name="glossary"),
    path("progress/", views.progress, name="progress"),
]
