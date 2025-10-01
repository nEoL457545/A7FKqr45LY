# 代码生成时间: 2025-10-02 02:50:22
# live_streaming_app/models.py
from django.db import models
from django.core.validators import URLValidator

class Stream(models.Model):
    """Model to store information about a live stream."""
    title = models.CharField(max_length=255)
    stream_key = models.CharField(max_length=255)
    stream_url = models.CharField(max_length=255, validators=[URLValidator()])
    
    def __str__(self):
        return self.title


# live_streaming_app/views.py
from django.http import JsonResponse
from .models import Stream
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError

@require_http_methods(['POST'])
def create_stream(request):
    """View to create a new live stream."""
    try:
        title = request.POST.get('title')
        stream_key = request.POST.get('stream_key')
        stream_url = request.POST.get('stream_url')
        
        stream = Stream.objects.create(
            title=title,
            stream_key=stream_key,
            stream_url=stream_url
        )
        
        return JsonResponse({'id': stream.id, 'message': 'Stream created successfully.'})
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

@require_http_methods(['GET'])
def get_stream(request, stream_id):
    """View to retrieve a live stream by its ID."""
    try:
        stream = Stream.objects.get(pk=stream_id)
        return JsonResponse({'title': stream.title, 'stream_url': stream.stream_url})
    except Stream.DoesNotExist:
        return JsonResponse({'error': 'Stream not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

# live_streaming_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_stream, name='create_stream'),
    path('<int:stream_id>/', views.get_stream, name='get_stream'),
]

# live_streaming_app/admin.py
from django.contrib import admin
from .models import Stream

admin.site.register(Stream)
