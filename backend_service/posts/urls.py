from django.urls import path, include
from . import views

urlpatterns = [
    path('bigfoot/', views.all_bigfoot, name='all_bigfoot'),
    path('bigfoot/user/<int:user_id>/', views.user_bigfoot, name='user_bigfoot'),
    path('bigfoot/create/', views.create_bigfoot, name='create_bigfoot'),
    path('bigfoot/<int:pk>/update/', views.update_bigfoot, name='update_bigfoot'),
    path('bigfoot/<int:pk>/delete/', views.delete_bigfoot, name='delete_bigfoot'),
    
    path('ufo/', views.all_ufo, name='all_ufo'),
    path('ufo/user/<int:user_id>/', views.user_ufo, name='user_ufo'),
    path('ufo/create/', views.create_ufo, name='create_ufo'),
    path('ufo/<int:pk>/update/', views.update_ufo, name='update_ufo'),
    path('ufo/<int:pk>/delete/', views.delete_ufo, name='delete_ufo'),
    
    path('ghosts/', views.all_ghosts, name='all_ghosts'),
    path('ghosts/user/<int:user_id>/', views.user_ghosts, name='user_ghosts'),
    path('ghosts/create/', views.create_ghost, name='create_ghost'),
    path('ghosts/<int:pk>/update/', views.update_ghost, name='update_ghost'),
    path('ghosts/<int:pk>/delete/', views.delete_ghost, name='delete_ghost'),
    
    path('others/', views.all_others, name='all_others'),
    path('others/user/<int:user_id>/', views.user_others, name='user_others'),
    path('others/create/', views.create_other, name='create_other'),
    path('others/<int:pk>/update/', views.update_other, name='update_other'),
    path('others/<int:pk>/delete/', views.delete_other, name='delete_other'),
]
