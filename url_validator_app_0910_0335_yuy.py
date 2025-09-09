# 代码生成时间: 2025-09-10 03:35:54
from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import path
from django.views import View
from urllib.parse import urlparse
import validators

# models.py
class URL(models.Model):
    """
    A simple model to store URLs to be validated.
    """
    url = models.URLField(max_length=255, unique=True)

    def __str__(self):
        return self.url

# views.py
class ValidateURLView(View):
    """
    A view to validate the URL link effectiveness.
    """
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to validate a URL.
        """
        url_to_validate = request.GET.get('url')
        if not url_to_validate:
            return JsonResponse({'error': 'URL is required'}, status=400)

        if not validators.url(url_to_validate):
            return JsonResponse({'error': 'Invalid URL'}, status=400)

        # Here you would typically save the URL to your database and perform further processing.
        # For this example, we'll just return a success message.
        url = URL(url=url_to_validate)
        url.save()

        return JsonResponse({'message': 'URL validated successfully'}, status=200)

# urls.py
urlpatterns = [
    path('validate-url/', ValidateURLView.as_view(), name='validate-url'),
]
