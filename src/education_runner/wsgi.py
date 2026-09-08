"""WSGI entry point for the standalone runner."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "education_runner.settings")
application = get_wsgi_application()
