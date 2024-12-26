"""Tests for the views in the core app."""

from __future__ import annotations

import os

import pytest

from core.models import User


@pytest.mark.django_db
def test_custom_user_model() -> None:
    """Test that the custom user model is used."""
    random_email: str = f"{os.urandom(8).hex()}@example.com"
    random_password: str = os.urandom(8).hex()
    random_username: str = os.urandom(8).hex()

    assert_msg: str = f"User with email {random_email} was not created."
    assert User.objects.create_user(email=random_email, password=random_password, username=random_username), assert_msg
    assert User.objects.get(email=random_email), f"User with email {random_email} was not found."
    assert User.objects.get(username=random_username), f"User with username {random_username} was not found."

    assert_msg = f"User with email {random_email} has wrong password."
    assert User.objects.get(email=random_email).check_password(random_password), assert_msg

    assert_msg = f"User with username {random_username} has wrong password."
    assert User.objects.get(username=random_username).check_password(random_password), assert_msg
    assert User.objects.get(email=random_email).is_active, f"User with email {random_email} is not active."
    assert not User.objects.get(email=random_email).is_staff, f"User with email {random_email} is staff."
    assert not User.objects.get(email=random_email).is_superuser, f"User with email {random_email} is superuser."

    assert_msg = f"User with email {random_email} has no usable password."
    assert User.objects.get(email=random_email).has_usable_password(), assert_msg

    assert_msg = f"User with email {random_email} has wrong email."
    assert User.objects.get(email=random_email).email == random_email, assert_msg

    assert_msg = f"User with username {random_username} has wrong username."
    assert User.objects.get(username=random_username).get_username() == random_username, assert_msg
