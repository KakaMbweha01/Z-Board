from django.shortcuts import render, redirect
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login

# Create your views here.

# notification view
@login_required
def notification_list(request):
    notifications = Notification.objects.all().order_by('-created_at')

    if request.method =='POST':
        if request.user.is_staff: # only staff can post
            title = request.POST.get('title')
            message = request.POST.get('message')
            if title and message:
                Notification.objects.create(title=title, message=message)
                return redirect('notification_list')

    return render(request, 'notifications/list.html', {'notifications': notifications})

# signup view for students
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'auth/signup.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        login(request, user) # login automatically after signup
        return redirect('notification_list')

    return render(request, 'auth/signup.html')