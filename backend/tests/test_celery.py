from django.conf import settings

from config import celery_app


def test_celery_app_reads_broker_url_from_settings() -> None:
    assert celery_app.conf.broker_url == settings.CELERY_BROKER_URL


def test_autodiscovery_registers_core_ping() -> None:
    celery_app.loader.import_default_modules()
    assert "core.ping" in celery_app.tasks


def test_ping_returns_pong() -> None:
    celery_app.loader.import_default_modules()
    assert celery_app.tasks["core.ping"].apply().get() == "pong"
