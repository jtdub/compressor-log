from django.test import Client


def test_schema_lists_health_and_config_paths(client: Client) -> None:
    response = client.get("/api/schema/?format=json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/api/v1/health/" in paths
    assert "/api/v1/config/" in paths


def test_docs_page_returns_200(client: Client) -> None:
    assert client.get("/api/docs/").status_code == 200
