from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import BasePermission
from .models import Notice
from .serializers import NoticeSerializer

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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.username)

# retrieve, update or delete a notice
class NoticeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer