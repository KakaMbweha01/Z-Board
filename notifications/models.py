from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

# notification model
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

# user model to distinguish admin and students
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

def __str__(self):
    return f"{self.title} ({self.get_category_display()})"