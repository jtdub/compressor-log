"""Serializers that describe the responses of the core API."""

from rest_framework import serializers


class HealthSerializer(serializers.Serializer[dict[str, str]]):
    """Describe the response of the health endpoint."""

    status = serializers.CharField()


class ConfigSerializer(serializers.Serializer[dict[str, bool]]):
    """Describe the response of the config endpoint."""

    saas_mode = serializers.BooleanField()
