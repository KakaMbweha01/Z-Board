from django.contrib import admin
from .models import Notice, Category

# Register your models here.

admin.site.register(Notice)
admin.site.register(Category)