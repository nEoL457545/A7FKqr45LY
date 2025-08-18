# 代码生成时间: 2025-08-18 11:32:47
# permission_management_system
# This Django application manages user permissions.

"""
Django application for managing user permissions.
This application handles the creation, modification, and
retrieval of user permissions within a Django project.
"""

# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Permission(models.Model):
    """
    A model representing a user permission.
    Each permission is linked to a user and a specific action.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissions')
    action = models.CharField(max_length=100)

    def clean(self):
        """
        Validates the permission instance.
        """
        if not self.user or not self.action:
            raise ValidationError("Permission requires a user and an action.")

    def __str__(self):
        """
        Returns a string representation of the permission.
        """
        return f"{self.user} - {self.action}"

# views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied
from .models import Permission
from django.contrib.auth.decorators import login_required

@login_required
@require_http_methods(['GET', 'POST'])
def permission_view(request):
    """
    A view to handle user permission management.
    It allows users to view and create permissions.
    """
    if request.method == 'GET':
        # Retrieve all permissions for the logged-in user
        permissions = Permission.objects.filter(user=request.user)
        return JsonResponse({'permissions': list(permissions.values())})
    elif request.method == 'POST':
        # Create a new permission for the logged-in user
        try:
            action = request.POST.get('action')
            permission = Permission.objects.create(user=request.user, action=action)
            return JsonResponse({'message': 'Permission created successfully.'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=405)

# urls.py
from django.urls import path
from .views import permission_view

urlpatterns = [
    path('permissions/', permission_view, name='permission_management'),
]
