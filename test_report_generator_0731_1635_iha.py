# 代码生成时间: 2025-07-31 16:35:30
# test_report_generator\application

"""
Django application for generating test reports.
"""

# models.py
"""
Model definitions for the test report generator.
"""

from django.db import models

class TestReport(models.Model):
    """
    Model representing a test report.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the TestReport model.
        """
        return self.title

# views.py
"""
Views for the test report generator.
"""

from django.shortcuts import render
from django.http import JsonResponse
from .models import TestReport

def generate_report(request):
    """
    View function to generate a test report.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        try:
            report = TestReport(title=title, description=description)
            report.save()
            return JsonResponse({'message': 'Report generated successfully.', 'id': report.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method. Use POST to generate a report.'})

# urls.py
"""
URL patterns for the test report generator.
"""

from django.urls import path
from .views import generate_report

urlpatterns = [
    path('generate/', generate_report, name='generate-report'),
]
