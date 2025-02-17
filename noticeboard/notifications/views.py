from django.shortcuts import render
from .models import Notification

# Create your views here.

# notification view
def notification_list(request):
    notifications = Notification.objects.all().order_by('-created_at')
    return render(request, 'notifications/list.html', {'notifications': notifications})