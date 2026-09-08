"""Django application configuration."""

from django.apps import AppConfig


class EducationRuntimeConfig(AppConfig):
    """Configure the shared, target-independent education runtime."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "education_runtime"
    verbose_name = "Education Runtime"
