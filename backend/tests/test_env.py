import pytest
from django.core.exceptions import ImproperlyConfigured

from config.env import env_bool, secret_key


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("1", True),
        ("true", True),
        ("TRUE", True),
        ("yes", True),
        ("on", True),
        ("  True  ", True),
        ("0", False),
        ("false", False),
        ("no", False),
        ("off", False),
        (" OFF ", False),
    ],
)
def test_env_bool_reads_true_and_false_values(
    monkeypatch: pytest.MonkeyPatch, raw: str, expected: bool
) -> None:
    monkeypatch.setenv("FLAG", raw)
    assert env_bool("FLAG", not expected) is expected


@pytest.mark.parametrize("default", [True, False])
def test_env_bool_returns_default_when_missing_or_empty(
    monkeypatch: pytest.MonkeyPatch, default: bool
) -> None:
    monkeypatch.delenv("FLAG", raising=False)
    assert env_bool("FLAG", default) is default
    monkeypatch.setenv("FLAG", "")
    assert env_bool("FLAG", default) is default
    monkeypatch.setenv("FLAG", "   ")
    assert env_bool("FLAG", default) is default


def test_env_bool_raises_on_unknown_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SAAS_MODE", "ture")
    with pytest.raises(ImproperlyConfigured, match="SAAS_MODE"):
        env_bool("SAAS_MODE", False)


@pytest.mark.parametrize("raw", [None, ""])
def test_secret_key_raises_when_missing_or_empty_and_debug_is_false(
    monkeypatch: pytest.MonkeyPatch, raw: str | None
) -> None:
    if raw is None:
        monkeypatch.delenv("DJANGO_SECRET_KEY", raising=False)
    else:
        monkeypatch.setenv("DJANGO_SECRET_KEY", raw)
    with pytest.raises(ImproperlyConfigured, match="DJANGO_SECRET_KEY"):
        secret_key(debug=False)


@pytest.mark.parametrize("raw", [None, ""])
def test_secret_key_returns_development_key_when_debug_is_true(
    monkeypatch: pytest.MonkeyPatch, raw: str | None
) -> None:
    if raw is None:
        monkeypatch.delenv("DJANGO_SECRET_KEY", raising=False)
    else:
        monkeypatch.setenv("DJANGO_SECRET_KEY", raw)
    assert secret_key(debug=True) == "django-insecure-development-only"


def test_secret_key_returns_the_variable_when_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DJANGO_SECRET_KEY", "abc")
    assert secret_key(debug=False) == "abc"
