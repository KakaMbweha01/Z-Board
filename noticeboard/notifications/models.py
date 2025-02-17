from django.db import models
from django.utils.timezone import now

# Create your models here.

# notification model
class Notification(models.Model):
    title = models.CharField(max_length=255)
    message= models.TextField()
    created_at = models.DateTimeField(default=now)

def __str__(self):
    return self.title