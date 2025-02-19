from django.urls import path
from .views import notification_list, user_login, user_logout, register, add_notification, edit_notification, delete_notification
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', notification_list, name='notification_list'),
    path('add/', add_notification, name='add_notification'),
    path('edit/<int:pk>/', edit_notification, name='edit_notification'),
    path('delete/<int:pk>/', delete_notification, name='delete_notification'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('register/', register, name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
]
