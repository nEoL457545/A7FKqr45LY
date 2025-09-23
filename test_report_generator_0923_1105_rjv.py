# 代码生成时间: 2025-09-23 11:05:23
from django.db import models


# Create your models here.

class TestReport(models.Model):
    """
    Represents a test report, which includes the test case name, 
    the date of creation, and the test results.
    """
    test_case_name = models.CharField(max_length=255, help_text="The name of the test case.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time the report was created.")
    test_result = models.TextField(help_text="The detailed results of the test.")

    def __str__(self):
        return f"{self.test_case_name} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


<!-- views.py -->
"""
Contains the views for the Test Report Generator application.
"""
from django.shortcuts import render
from django.http import HttpResponse
from .models import TestReport

# Create your views here.

def generate_report(request):
    """
    Handles the GET request to generate a test report.
    """
    if request.method == 'GET':
        reports = TestReport.objects.all()
        context = {'reports': reports}
        return render(request, 'test_reports/report_list.html', context)
    else:
        return HttpResponse("Invalid request method.", status=405)



<!-- urls.py -->
"""
Defines the URL patterns for the Test Report Generator application.
"""
from django.urls import path
from .views import generate_report

# Create your URLs here.

urlpatterns = [
    path('reports/', generate_report, name='generate_report'),
]


<!-- report_list.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Test Reports</title>
</head>
<body>
    <h1>Test Reports</h1>
    <ul>
        {% for report in reports %}
            <li>{{ report.test_case_name }} - {{ report.created_at }} - {{ report.test_result }}</li>
        {% endfor %}
    </ul>
</body>
</html>