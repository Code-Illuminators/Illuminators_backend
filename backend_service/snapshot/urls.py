from django.urls import path
from . import views
urlpatterns = [
    path('backup/', views.backup_posts, name='backup_posts'),
    path('restore/', views.restore_posts, name='restore_posts'),
]
