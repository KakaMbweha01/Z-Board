from django.shortcuts import render, redirect, get_object_or_404
from .models import Notification
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import NotificationForm
from django.http import HttpResponse

# Create your views here.

# notification view
@login_required
def notification_list(request):
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')

    notifications = Notification.objects.all().order_by('-created_at')

    if request.method =='POST':
        if request.user.is_staff: # only staff can post
            title = request.POST.get('title')
            message = request.POST.get('message')
            category = request.POST.get('category', 'general')

            if title and message:
                Notification.objects.create(
                    title=title,
                    message=message,
                    category=category
                    )
                # get students emails except staff
                ##student_emails = User.objects.filter(is_staff=False).values_list('email', flat=True)
                student_emails = list(User.objects.filter(is_staff=False)
                                      .exclude(email="")
                                      .values_list('email', flat=True)
                                      )
                # send emails to students
                if student_emails:
                    send_mail(
                        subject=f"New Notification: {title}",
                        message=message,
                        from_email='leonestill804@gmail.com',
                        recipient_list=student_emails,
                        fail_silently=False,
                    )
                return redirect('notification_list')
    if query:
        notifications = notifications.filter(Q(title__icontains=query) | Q(message__icontains=query))

    if category_filter:
        notifications = notifications.filter(category=category_filter)

    for notification in notifications:
        if hasattr(notification, 'is_read_by'):
            notification.is_read = notification.is_read_by(request.user)

    paginator = Paginator(notifications, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)



    return render(request, 'notifications/list.html', {
        'notifications': page_obj,
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

# user login view
def user_login(request):
    #if request.user.is_authenticated:
        #return redirect('notification_list')
    #print("RENDERING LOGIN PAGE ....") debugging code!
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('notification_list')
    else:
        form = AuthenticationForm()
    return render(request, 'notifications/login.html', {'form': form})

# user logout view
def user_logout(request):
    logout(request)
    return redirect('user_login')

# student registration
def register(request):
    if request.user.is_authenticated:
        return redirect('notification_list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('notification_list')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

# role based restriction
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

# list all notifications (Admin Only)
@login_required
@user_passes_test(is_admin)
def notification_list_admin(request):
    notifications = Notification.objects.all()
    return render(request, "notifications/admin_notification_list.html", {"notifications": notifications})

# adding a notification
@login_required
@user_passes_test(is_admin)
def add_notification(request):
    if request.method == "POST":
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            #notification.user = request.user  # Assign the logged-in user before saving
            # ensure a user is selected from the form
            if form.cleaned_data.get('user'):
                notification.user = form.cleaned_data['user']
            else:
                return HttpResponse("Error: A recipient must be selected.")
            notification.save()
            #form.save()
            return redirect('admin_notifications')
    else:
        form = NotificationForm()

    return render(request, 'notifications/add_notification.html', {'form': form })

# edit a notification
@login_required
@user_passes_test(is_admin)
def edit_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)

    if request.method == "POST":
        form = NotificationForm(request.POST, instance=notification)
        if form.is_valid():
            form.save()
            return redirect('admin_notifications')
    else:
        form = NotificationForm(instance=notification)

    return render(request, 'notifications/edit_notification.html', {'form': form })

# delete a notification
@login_required
@user_passes_test(is_admin)
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)

    if request.method == "POST":
        notification.delete()
        return redirect('admin_notifications')

    return render(request, 'notifications/delete_notification.html', {'notification': notification })

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.read_by.add(request.user)
    return redirect('notification_list')

def home(request):
    notifications = Notification.objects.all().order_by('-created_at')[:5]
    return render(request, 'notifications/home.html', {'notifications': notifications })