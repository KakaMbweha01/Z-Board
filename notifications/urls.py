from django.urls import path
#from .views import (notification_list, user_login, user_logout, register, add_notification, edit_notification, delete_notification, mark_as_read, notification_list_admin)
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('notfications/', views.notification_list, name='notification_list'),
    path('admin/notifications/', views.notification_list_admin, name='admin_notifications'),
    path('admin/notifications/add/', views.add_notification, name='add_notification'),
    path('admin/notifications/edit/<int:notification_id>/', views.edit_notification, name='edit_notification'),
    path('admin/notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.register, name='register'),
    path('read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
]
