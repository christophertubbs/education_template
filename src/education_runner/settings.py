"""Environment-driven standalone settings; curriculum logic lives elsewhere."""

from __future__ import annotations

import os
from pathlib import Path
import socket

from django.conf.global_settings import STORAGES

from .product_discovery import discover_product_apps

BASE_DIR = Path(__file__).resolve().parents[2]
SECRET_KEY = os.environ.get("EDUCATION_SECRET_KEY", "unsafe-development-key")
DEBUG = os.environ.get("EDUCATION_DEBUG", "true").lower() == "true"
ALLOWED_HOSTS = [
    value.strip()
    for value in os.environ.get("EDUCATION_ALLOWED_HOSTS", f"localhost,127.0.0.1,{socket.gethostname()}").split(
        ","
    )
    if value.strip()
]


PRODUCT_APPS = discover_product_apps(os.environ.get("EDUCATION_PRODUCTS", ""))
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "education_runtime.apps.EducationRuntimeConfig",
    *PRODUCT_APPS,
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "education_runner.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
WSGI_APPLICATION = "education_runner.wsgi.application"
ASGI_APPLICATION = "education_runner.asgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": Path(
            os.environ.get("EDUCATION_DATABASE", BASE_DIR / "education.sqlite3")
        ),
    }
}

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    }
}

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
