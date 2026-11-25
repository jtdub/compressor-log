"""Read typed values from the process environment."""

import os

from django.core.exceptions import ImproperlyConfigured

TRUE_VALUES = frozenset({"1", "true", "yes", "on"})
FALSE_VALUES = frozenset({"0", "false", "no", "off"})
DEVELOPMENT_SECRET_KEY = "django-insecure-development-only"


def env_bool(name: str, default: bool) -> bool:
    """Return the boolean value of an environment variable.

    Raises:
        ImproperlyConfigured: If the value is not a known boolean text.
    """
    raw = os.environ.get(name, "").strip().lower()
    if not raw:
        return default
    if raw in TRUE_VALUES:
        return True
    if raw in FALSE_VALUES:
        return False
    raise ImproperlyConfigured(f"{name} must be a boolean value, not {raw!r}.")


def secret_key(debug: bool) -> str:
    """Return the Django secret key.

    Raises:
        ImproperlyConfigured: If the key is empty and debug is false.
    """
    value = os.environ.get("DJANGO_SECRET_KEY", "").strip()
    if value:
        return value
    if debug:
        return DEVELOPMENT_SECRET_KEY
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY is required when DJANGO_DEBUG is false."
    )
