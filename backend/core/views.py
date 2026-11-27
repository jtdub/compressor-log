"""Views of the core app."""

from django.conf import settings
from django.db import Error, connection
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from core.serializers import ConfigSerializer, HealthSerializer


@extend_schema(responses={200: HealthSerializer, 503: HealthSerializer})
@api_view(["GET"])
@permission_classes([AllowAny])
def health(request: Request) -> Response:
    """Return 200 when the database answers and 503 when it does not."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Error:
        return Response(
            {"status": "unavailable"}, status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    return Response({"status": "ok"})


@extend_schema(responses={200: ConfigSerializer})
@api_view(["GET"])
@permission_classes([AllowAny])
def config(request: Request) -> Response:
    """Return the public settings of the deployment."""
    return Response({"saas_mode": settings.SAAS_MODE})
