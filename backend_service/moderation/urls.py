from django.urls import path
from . import views

urlpatterns = [
    path('votes/create/', views.create_vote, name='create-vote'),
    path('votes/active/', views.votes_list, name='votes-list'),
    path('votes/<int:pk>/vote/', views.collect_vote, name='collect-vote'),
    path('votes/<int:pk>/delete/', views.delete_vote, name='delete-vote'),
    path('votes/result/<str:username>/delete/', views.delete_user_account, name='delete-user'),
    path('delete-all/', views.delete_all, name='delete_all_data'),
]