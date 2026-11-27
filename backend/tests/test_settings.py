from typing import Any

import pytest
from django.conf import settings
from django.test import Client


def test_default_permission_is_is_authenticated() -> None:
    permissions = settings.REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"]
    assert permissions == ["rest_framework.permissions.IsAuthenticated"]


def test_database_has_connect_timeout() -> None:
    database: dict[str, Any] = settings.DATABASES["default"]
    assert database["OPTIONS"]["connect_timeout"] == 5


def test_unknown_host_returns_400(client: Client) -> None:
    assert client.get("/api/v1/health/", HTTP_HOST="evil.test").status_code == 400


@pytest.mark.django_db
def test_allowed_host_from_environment_returns_200(client: Client) -> None:
    assert client.get("/api/v1/health/", HTTP_HOST="localhost").status_code == 200
