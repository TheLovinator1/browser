from __future__ import annotations

import logging

from django.contrib.auth.models import AbstractUser

logger: logging.Logger = logging.getLogger(__name__)


class User(AbstractUser):
    """Custom User model."""
