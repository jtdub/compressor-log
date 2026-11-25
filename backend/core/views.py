"""Views of the core app."""

from django.db import Error, connection
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response


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
