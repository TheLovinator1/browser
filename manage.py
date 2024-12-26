#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

from __future__ import annotations

import logging
import os
import sys

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        msg = (
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
        logger.exception(msg)
        raise ImportError(msg) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
