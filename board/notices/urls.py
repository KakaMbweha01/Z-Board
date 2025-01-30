from django.urls import path
from .views import NoticeListCreateView, NoticeDetailView

urlpatterns = [
    path('notices/', NoticeListCreateView.as_view(), name='notice-list'),
    path('notices/<int:pk>/', NoticeDetailView.as_view(), name='notice-detail'),
]
