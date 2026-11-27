"""App configuration of the core app."""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configure the core app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
