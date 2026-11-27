"""Celery tasks of the core app."""

from celery import shared_task


@shared_task(name="core.ping")
def ping() -> str:
    """Return the text "pong"."""
    return "pong"
