from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from platformdirs import user_data_dir

load_dotenv(verbose=True)

BASE_DIR: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = Path(user_data_dir(appname="browser_api", appauthor="TheLovinator", roaming=True))
SECRET_KEY: str = os.getenv("DJANGO_SECRET_KEY", default="")
if not SECRET_KEY:
    msg = "DJANGO_SECRET_KEY not set"
    raise ValueError(msg)

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
DEBUG: bool = os.getenv("DJANGO_DEBUG", default="False").lower() == "true"
ALLOWED_HOSTS: list[str] = ["*"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS: list[str] = [
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


DATABASES = {
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
