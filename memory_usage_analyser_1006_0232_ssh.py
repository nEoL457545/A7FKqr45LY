# 代码生成时间: 2025-10-06 02:32:20
from django.db import models
from django.http import JsonResponse
import psutil
# 优化算法效率
import os
# 扩展功能模块
import json

"""
A Django application component for memory usage analysis.
"""

class MemoryUsage(models.Model):
    """
    Model to capture memory usage data.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    memory_info = models.JSONField()

    def __str__(self):
        return f"MemoryUsage at {self.timestamp}"


def get_memory_usage(request):
    """
    View function to get current memory usage and save it to the database.
    
    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing memory usage data.
    """
    if request.method == 'GET':
        try:
            # Get memory usage details from psutil
            memory = psutil.virtual_memory()
            # Create a dictionary to hold memory usage data
            memory_data = {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'free': memory.free,
# 增强安全性
                'percent': memory.percent,
            }
            # Create and save a new MemoryUsage instance
            MemoryUsage.objects.create(memory_info=memory_data)
            # Return JSON response with memory usage data
            return JsonResponse(memory_data)
        except Exception as e:
            # Handle any exceptions and return error message
# 增强安全性
            return JsonResponse({'error': str(e)})
    else:
        # If the request is not a GET, return an error response
        return JsonResponse({'error': 'Method not allowed'}, status=405)
# 增强安全性


# Define the URL patterns for the memory_usage_analyser app
from django.urls import path

urlpatterns = [
    path('memory_usage/', get_memory_usage, name='memory_usage'),
]
# 添加错误处理
