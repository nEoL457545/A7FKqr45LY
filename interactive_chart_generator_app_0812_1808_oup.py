# 代码生成时间: 2025-08-12 18:08:23
# interactive_chart_generator_app.py
"""
Django application component for generating interactive charts.

This application provides functionality for creating and displaying interactive charts.
It includes models for data storage, views for handling requests, and URLs for routing.
"""

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import path
from .models import ChartData
import json
import chart_js

# Models
class ChartData(models.Model):
    """
    Model to store chart data.
    """
    title = models.CharField(max_length=255)
    data = models.JSONField()

    def __str__(self):
        return self.title

# Views
class ChartGeneratorView(View):
    """
    View to generate and display interactive charts.
    """
    def get(self, request, *args, **kwargs):
        """
        Generate and display an interactive chart.
        """
        try:
            # Fetch data from ChartData model
            chart_data = ChartData.objects.all()
            # Create a ChartJS chart
            chart = chart_js.Chart(
                type="bar",
                data=chart_data[0].data if chart_data else {}
            )
            # Render chart in HTML
            chart_html = chart.render()
            # Return the chart HTML
            return render(request, 'chart.html', {'chart_html': chart_html})
        except Exception as e:
            # Handle errors and return an error message
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request, *args, **kwargs):
        """
        Create a new chart data entry.
        """
        try:
            # Get chart data from request body
            chart_data = json.loads(request.body)
            # Create a new ChartData instance
            chart = ChartData.objects.create(title=chart_data['title'], data=chart_data['data'])
            # Return a success message
            return JsonResponse({'message': 'Chart created successfully'}, status=201)
        except Exception as e:
            # Handle errors and return an error message
            return JsonResponse({'error': str(e)}, status=400)

# URLs
urlpatterns = [
    path('chart/', ChartGeneratorView.as_view(), name='chart_generator'),
]
