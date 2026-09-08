"""ASGI entry point for the standalone runner."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "education_runner.settings")
application = get_asgi_application()
