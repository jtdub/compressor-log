from typing import Any

from django.conf import settings


def test_default_permission_is_is_authenticated() -> None:
    permissions = settings.REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"]
    assert permissions == ["rest_framework.permissions.IsAuthenticated"]


def test_database_has_connect_timeout() -> None:
    database: dict[str, Any] = settings.DATABASES["default"]
    assert database["OPTIONS"]["connect_timeout"] == 5
