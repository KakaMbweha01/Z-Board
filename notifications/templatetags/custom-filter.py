from django import template
#from notifications.models import Notification

register = template.Library()

@register.filter
def is_read(notification, user): # check if notifcation is read by given user
    if notification is None:
        return False
    return notification.is_read_by(user)
