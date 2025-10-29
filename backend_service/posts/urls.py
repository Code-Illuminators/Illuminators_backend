"""Configuring the path."""
from django.urls import path
from . import views
POST_TYPES = ["bigfoot", "ufo", "ghosts", "others"]
urlpatterns = []
for post_type in POST_TYPES:
    urlpatterns.extend([
        path(f'{post_type}/', getattr(views, f"all_{post_type}"), name=f'all_{post_type}'),
        path(f'{post_type}/user/<int:user_id>/', getattr(views, f"user_{post_type}"), name=f'user_{post_type}'),
        path(f'{post_type}/create/', getattr(views, f"create_{post_type}"), name=f'create_{post_type}'),
        path(f'{post_type}/<int:pk>/update/', getattr(views, f"update_{post_type}"), name=f'update_{post_type}'),
        path(f'{post_type}/<int:pk>/delete/', getattr(views, f"delete_{post_type}"), name=f'delete_{post_type}'),
    ])
