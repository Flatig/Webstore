from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.account_menu, name='account_menu'),
    path('register/', views.register_view, name='register'),
    path('register/done/<int:user_id>/', views.register_done, name='register_done'),
    path('login/', views.login_view, name='login'),
    path('profile:<str:username>/', views.profile_view, name='profile'),
    path('profile:<str:username>/edit/', views.edit_view, name='edit'),
    path('logout/', views.logout_view, name='logout'),

    # Password URLs are based on django.contrib.auth, but the URL and template path have been changed.
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='account/password/password_change_form.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password/password_change_done.html'), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='account/password/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password/password_reset_complete.html'),
         name='password_reset_complete'),
]
