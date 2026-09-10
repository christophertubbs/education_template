"""Sphinx configuration for the education curriculum system."""

from __future__ import annotations

import sys
from pathlib import Path

import django
from django.conf import settings

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = REPOSITORY_ROOT / "src"
sys.path.insert(0, str(SOURCE_ROOT))

# Autodoc imports Django model modules.  A minimal in-memory configuration keeps
# documentation builds independent of local databases and generated products.
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "education_runtime.apps.EducationRuntimeConfig",
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        SECRET_KEY="documentation-build-only",
        ROOT_URLCONF="education_runtime.urls",
        DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
    )
django.setup()

project = "Education Curriculum System"
author = "Education Curriculum System contributors"
release = "1.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

root_doc = "index"
templates_path: list[str] = []
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "alabaster"
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_preserve_defaults = True
add_module_names = False
