from django.shortcuts import render, redirect
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

# notification view
@login_required
def notification_list(request):
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')

    notifications = Notification.objects.all().order_by('-created_at')

    if query:
        notifications = notifications.filter(Q(title_icontains=query) | Q(message_icontains=query))

    if category_filter:
        notifications = notifications.filter(category=category_filter)

    paginator = Paginator(notifications, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.method =='POST':
        if request.user.is_staff: # only staff can post
            title = request.POST.get('title')
            message = request.POST.get('message')
            category = request.POST.get('category', 'general')

            if title and message:
                Notification.objects.create(title=title, message=message)
                # get students emails except staff
                student_emails = User.objects.filter(is_staff=False).values_list('email', flat=True)
                # send emails to students
                send_mail(
                    subject=f"New Notification: {title}",
                    message=message,
                    from_email='leonestill804@gmail.com',
                    recipient_list=student_emails,
                    fail_silently=False,
                )
                return redirect('notification_list')

    return render(request, 'notifications/list.html', {
        'notifications': notifications,
        'query': query,
        'category_filter': category_filter,
        })

# signup view for students
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST.get['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            return render(request, 'auth/signup.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        login(request, user) # login automatically after signup
        return redirect('notification_list')

    return render(request, 'auth/signup.html')