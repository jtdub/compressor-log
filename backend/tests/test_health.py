from unittest.mock import MagicMock, patch

import pytest
from django.db import OperationalError
from django.test import Client


@pytest.mark.django_db
def test_health_returns_ok_when_database_answers(client: Client) -> None:
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_returns_503_when_database_is_down(client: Client) -> None:
    broken_connection = MagicMock()
    broken_connection.cursor.side_effect = OperationalError("database is down")
    with patch("core.views.connection", broken_connection):
        response = client.get("/api/v1/health/")
    assert response.status_code == 503
    assert response.json() == {"status": "unavailable"}


@pytest.mark.django_db
def test_health_needs_no_authentication(client: Client) -> None:
    assert "Authorization" not in client.defaults
    assert client.get("/api/v1/health/").status_code == 200
