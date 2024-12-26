from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from platformdirs import user_data_dir

logger: logging.Logger = logging.getLogger(__name__)

load_dotenv(verbose=True)

GITHUB_ACCESS_TOKEN: str = os.getenv("GITHUB_ACCESS_TOKEN", default="")
if not GITHUB_ACCESS_TOKEN:
    msg = "GITHUB_ACCESS_TOKEN not set"
    raise ValueError(msg)

BASE_DIR: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = Path(user_data_dir(appname="browser_api", appauthor="TheLovinator", roaming=True, ensure_exists=True))
SECRET_KEY: str = os.getenv("DJANGO_SECRET_KEY", default="")
if not SECRET_KEY:
    msg = "DJANGO_SECRET_KEY not set"
    raise ValueError(msg)

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
DEBUG: bool = os.getenv("DJANGO_DEBUG", default="False").lower() == "true"
ALLOWED_HOSTS: list[str] = ["*"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SITE_ID = 1
INTERNAL_IPS: list[str] = ["127.0.0.1", "192.168.1.129"]
AUTH_USER_MODEL: Literal["core.User"] = "core.User"
STATIC_URL = "static/"
STATIC_ROOT: Path = BASE_DIR / "static"

INSTALLED_APPS: list[str] = [
    "core.apps.CoreConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


DATABASES: dict[str, dict[str, Path | str | dict[str, str | int]]] = {
    "default": {
        "NAME": DATA_DIR / "database.sqlite3",
        "ENGINE": "django.db.backends.sqlite3",
        "OPTIONS": {
            "transaction_mode": "IMMEDIATE",
            "timeout": 5,  # seconds
            "init_command": """
                PRAGMA journal_mode=WAL;
                PRAGMA synchronous=NORMAL;
                PRAGMA mmap_size = 134217728;
                PRAGMA journal_size_limit = 27103364;
                PRAGMA cache_size=2000;
            """,
        },
    }
}


AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGGING: dict[str, int | bool | dict[str, dict[str, str | list[str] | bool]]] = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django.utils.autoreload": {  # Remove spam
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

TEMPLATES: list[dict[str, str | list[Path] | bool | dict[str, list[str]]]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
