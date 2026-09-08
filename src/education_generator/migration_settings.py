"""Minimal Django settings used to derive a Curriculum App's migrations."""

from __future__ import annotations

import os


SECRET_KEY = "migration-generation-only"
INSTALLED_APPS = [os.environ["EDUCATION_CURRICULUM_APP"]]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
