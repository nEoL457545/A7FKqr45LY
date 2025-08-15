# 代码生成时间: 2025-08-16 07:01:48
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import json

# Models
class ExampleModel(models.Model):
    """Example model for demonstration purposes."""
    name = models.CharField(max_length=100, help_text="The name of the example.")
    description = models.TextField(blank=True, null=True, help_text="A brief description of the example.")
    
    def __str__(self):
        return self.name

# Views
class ExampleAPIView(View):
    """
    A simple API view to handle requests for ExampleModel.
    """
    def get(self, request):
        """
        Handles GET requests.
        """
        examples = ExampleModel.objects.all()
        serializer = []
        for example in examples:
            serializer.append({
                "id": example.id,
                "name": example.name,
                "description": example.description
            })
        return JsonResponse(serializer, safe=False)

    def post(self, request):
        """
        Handles POST requests.
        """
        data = json.loads(request.body)
        try:
            example = ExampleModel.objects.create(
                name=data.get('name'),
                description=data.get('description', '')
            )
            return JsonResponse({
                'id': example.id,
                'name': example.name,
                'description': example.description
            }, status=201)
        except (ValueError, ValidationError) as e:
            return JsonResponse({'error': str(e)}, status=400)

# URL Configuration
urlpatterns = [
    path('example/', method_decorator(csrf_exempt, name='dispatch')(ExampleAPIView.as_view()), name='api-example'),
]
