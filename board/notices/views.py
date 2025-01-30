from django.shortcuts import render
from rest_framework import generics
from .models import Notice
from .serializers import NoticeSerializer

# Create your views here.

# list all notices, create a new notice
class NoticeListCreateView(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

# retrieve, update or delete a notice
class NoticeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer