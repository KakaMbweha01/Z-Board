from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import BasePermission
from .models import Notice
from .serializers import NoticeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

# Create your views here.

# role-based permissions(admin only can create notices)
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

# list all notices, create a new notice
class NoticeListCreateView(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'date_posted']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(author__icontains=search_query)
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.username)

# retrieve, update or delete a notice
class NoticeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer