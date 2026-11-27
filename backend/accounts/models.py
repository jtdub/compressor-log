"""Models of the accounts app."""

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """The user of compressor-log. It adds no field to the Django user."""
