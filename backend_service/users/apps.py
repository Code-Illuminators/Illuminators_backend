"""Configuring the users application for Django."""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Class for UsersConfig."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
