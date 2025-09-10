# 代码生成时间: 2025-09-10 23:35:19
import psutil
from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.views import View

"""
Memory Analysis Application

This application is designed to analyze the memory usage of the server.
"""


class MemoryUsage(models.Model):
    """Model to store memory usage data."""
    timestamp = models.DateTimeField(auto_now_add=True)
    used_memory = models.FloatField()
    available_memory = models.FloatField()
    percent_used = models.FloatField()

    def __str__(self):
        return f"Memory at {self.timestamp}: {self.percent_used}% used"


class MemoryAnalysisView(View):
    """View to provide memory usage data."""
    def get(self, request, *args, **kwargs):
        try:
            mem = psutil.virtual_memory()
            used_memory = mem.used
            available_memory = mem.available
            percent_used = mem.percent

            MemoryUsage.objects.create(
                used_memory=used_memory,
                available_memory=available_memory,
                percent_used=percent_used,
            )

            data = {
                'used_memory': used_memory,
                'available_memory': available_memory,
                'percent_used': percent_used,
            }

            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# URL Configuration
urlpatterns = [
    path('memory-analysis/', MemoryAnalysisView.as_view(), name='memory_analysis'),
]
