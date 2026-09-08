"""Target-independent learner routes."""

from django.urls import path

from . import views

app_name = "education_runtime"

urlpatterns = [
    path("", views.curriculum_list, name="curriculum-list"),
    path("<slug:curriculum_id>/", views.curriculum_detail, name="curriculum-detail"),
    path(
        "<slug:curriculum_id>/lessons/<slug:lesson_id>/",
        views.lesson_detail,
        name="lesson",
    ),
    path(
        "<slug:curriculum_id>/assessments/<slug:assessment_id>/",
        views.assessment_detail,
        name="assessment",
    ),
    path("<slug:curriculum_id>/glossary/", views.glossary, name="glossary"),
    path("<slug:curriculum_id>/sources/", views.sources, name="sources"),
    path("<slug:curriculum_id>/progress/", views.progress, name="progress"),
]
