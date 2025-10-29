from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('users/', views.users_list, name='users'),
    path('login/', views.login_user, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('report-hunter-ip/', views.report_government_ip, name='report_government_ip'),
    path('entry-password/check/', views.check_entry_password, name='check_password'),
    path('entry-password/set/', views.set_entry_password, name='set_password'),
    path('entry-password/delete/<int:password_id>/', views.delete_entry_password, name='delete_password'),
    path('entry-password/active/', views.get_active_password, name='active_password'),
]
