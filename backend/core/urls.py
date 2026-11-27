"""URL routes of the core app."""

from django.urls import path

from core import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("config/", views.config, name="config"),
]
