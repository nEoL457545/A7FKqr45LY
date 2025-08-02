# 代码生成时间: 2025-08-02 17:01:06
from django.db import models
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.utils.module_loading import import_string
from urllib.parse import urlparse
import requests

"""
This Django app allows for the validation of URL links to check their validity.
"""

class Link(models.Model):
    url = models.URLField(unique=True)
    """Model representing a URL link."""

    def __str__(self):
        return self.url

@require_http_methods(['POST'])
def validate_url(request):
    '''
    View function to validate a URL link.
    It checks if the URL is valid and accessible.

    Args:
        request (HttpRequest): The HTTP request containing the URL to validate.

    Returns:
        JsonResponse: JSON response indicating the validity of the URL.
    '''
    try:
        data = request.POST
        url = data.get('url')
        if not url:
            return HttpResponseBadRequest("Missing 'url' parameter.")

        # Validate the URL format
        result = urlparse(url)
        if not all((result.scheme, result.netloc)):
            return HttpResponseBadRequest("Invalid URL format.")

        # Check if the URL is accessible
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            return JsonResponse({'message': 'URL is valid.', 'url': url})
        else:
            return JsonResponse({'message': 'URL is not valid.', 'status_code': response.status_code, 'url': url})
    except requests.RequestException as e:
        return HttpResponseBadRequest("Error checking URL: " + str(e))
    except Exception as e:
        return HttpResponseBadRequest("An unexpected error occurred: " + str(e))

# URLs configuration
url_patterns = [
    # Define the URL pattern for the 'validate_url' view
    path('validate/', validate_url, name='validate_url'),
]

# Example usage of the above view function within a Django project's urls.py
# from django.urls import path
# from . import views as link_validator_views
# urlpatterns = [
#     path('link-validator/validate/', link_validator_views.validate_url, name='validate_url'),
# ]