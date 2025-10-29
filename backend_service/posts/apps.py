"""Configuring the posts for Django."""
from django.apps import AppConfig


class PostsConfig(AppConfig):
    """Class for PostsConfig."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
