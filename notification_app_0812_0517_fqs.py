# 代码生成时间: 2025-08-12 05:17:56
# notification_app/models.py
from django.db import models
from django.contrib.auth.models import User

"""
Define the Notification model to store message notifications.
"""
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.message}"

# notification_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from .models import Notification
from django.contrib.auth.decorators import login_required

"""
Define views for Notification model.
"""
@require_http_methods(['GET'])
@login_required
def get_notifications(request):
    try:
        notifications = Notification.objects.filter(user=request.user)
        notifications_data = [
            {'message': notification.message, 'timestamp': notification.timestamp.strftime("%Y-%m-%d %H:%M:%S")}
            for notification in notifications
        ]
        return JsonResponse({'notifications': notifications_data}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# notification_app/urls.py
from django.urls import path
from . import views

"""
Define the URL patterns for Notification views.
"""
urlpatterns = [
    path('notifications/', views.get_notifications, name='get_notifications'),
]

# notification_app/admin.py
from django.contrib import admin
from .models import Notification

"""
Register the Notification model to Django admin interface.
"""
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp')
    search_fields = ('user__username', 'message')

# notification_app/apps.py
from django.apps import AppConfig

"""
Notification AppConfig class.
"""
class NotificationConfig(AppConfig):
    name = 'notification_app'
    verbose_name = 'Notification System'