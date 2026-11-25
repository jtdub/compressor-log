import pytest
from django.test import Client
from pytest_django.fixtures import Settings


@pytest.mark.django_db
def test_config_returns_saas_mode_false_by_default(
    client: Client, settings: Settings
) -> None:
    settings.SAAS_MODE = False
    response = client.get("/api/v1/config/")
    assert response.status_code == 200
    assert response.json() == {"saas_mode": False}


@pytest.mark.django_db
def test_config_returns_saas_mode_true_when_set(
    client: Client, settings: Settings
) -> None:
    settings.SAAS_MODE = True
    response = client.get("/api/v1/config/")
    assert response.json() == {"saas_mode": True}


@pytest.mark.django_db
def test_config_needs_no_authentication(client: Client) -> None:
    assert "Authorization" not in client.defaults
    assert client.get("/api/v1/config/").status_code == 200
