from django.db import models
from django.utils.timezone import now

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

def __str__(self):
    return f"{self.title} ({self.get_cateory_display()})"