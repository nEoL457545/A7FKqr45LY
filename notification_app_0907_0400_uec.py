# 代码生成时间: 2025-09-07 04:00:14
# notification_app
# A Django application for implementing a simple notification system.

"""
This Django application provides a basic notification system.
It includes models for storing notifications, views for handling
notifications, and URLs for routing.
"""

# models.py
from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    """Model for storing notification data."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.message}"

# views.py
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def mark_as_read(request, notification_id):
    """Mark a notification as read by the user."""
    notification = get_object_or_404(Notification, pk=notification_id, user=request.user)
    notification.read = True
    notification.save()
    return HttpResponse("Notification marked as read.")

@login_required
def get_unread_notifications(request):
    """Retrieve unread notifications for the user."""
    notifications = Notification.objects.filter(user=request.user, read=False)
    return render(request, 'unread_notifications.html', {'notifications': notifications})

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('unread_notifications/', views.get_unread_notifications, name='unread_notifications'),
]

# templates/unread_notifications.html
<!DOCTYPE html>
<html>
<head>
    <title>Unread Notifications</title>
</head>
<body>
    <h1>Unread Notifications</h1>
    <ul>
        {% for notification in notifications %}
            <li>{{ notification.message }}
                <a href="/mark_as_read/{{ notification.id }}/">Mark as Read</a>
            </li>
        {% empty %}
            <li>No unread notifications.</li>
        {% endfor %}
    </ul>
</body>
</html>