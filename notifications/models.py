from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.contrib.auth import get_user_model

# Create your models here.

# user model to distinguish admin and students
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

# notification model
User = get_user_model()
class Notification(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('exams', 'Exams'),
        ('events', 'Events'),
        ('deadlines', 'Deadlines'),
    ]

    title = models.CharField(max_length=255)
    message= models.TextField()
    created_at = models.DateTimeField(default=now)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='general')
    read_by = models.ManyToManyField(CustomUser, blank=True, related_name="read_notifications")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #is_read = models.BooleanField(default=False)

    def is_read_by(self, user):
        return self.read_by.filter(id=user.id).exists()


# mark as read
'''class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(CustomUser, blank=True, related_name="read_notifications")

    def is_read_by(self, user):
        return self.read_by.filter(id=user.id).exists()'''

def __str__(self):
    return f"{self.title} ({self.get_category_display()})"