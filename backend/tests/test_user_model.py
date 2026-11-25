import pytest
from django.contrib.auth import get_user_model
from pytest_django.fixtures import Settings

from accounts.models import User


def test_auth_user_model_is_accounts_user(settings: Settings) -> None:
    assert settings.AUTH_USER_MODEL == "accounts.User"
    assert get_user_model() is User


@pytest.mark.django_db
def test_create_user_saves_to_database() -> None:
    user = User.objects.create_user(username="operator", password="s3cret-pass")
    assert User.objects.get(pk=user.pk).username == "operator"
    assert user.check_password("s3cret-pass")
