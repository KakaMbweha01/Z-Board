from django.contrib import admin
from .models import Notification, CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# notif model
#admin.site.register(Notification)

# Register custom user in django admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)

# admin notifications
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'is_read_status']
    search_fields = ['title', 'user__username']
    list_filter = ['created_at']
    ordering = ['-created_at']

    def is_read_status(self, obj):
        return obj.is_read
    is_read_status.boolean = True
    is_read_status.short_description = "Read Status"

admin.site.register(Notification, NotificationAdmin)

admin.site.register(CustomUser, CustomUserAdmin)