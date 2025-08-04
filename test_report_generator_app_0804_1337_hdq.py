# 代码生成时间: 2025-08-04 13:37:48
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import path
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
import json

# Models
class TestCase(models.Model):
    """Model to store test case details."""
    name = models.CharField(max_length=100)
    description = models.TextField()


# Views
class TestReportView(View):
    """
    View to generate a test report.
    It takes test cases as input and generates a report based on the test results.
    """
    def get(self, request, *args, **kwargs):
        """
        Generate a test report as a JSON response.
        """
        test_cases = TestCase.objects.all()  # Retrieve all test cases
        report_data = []
        for case in test_cases:
            report_data.append({'name': case.name, 'description': case.description})

        return JsonResponse({'test_report': report_data}, safe=False)

    def post(self, request, *args, **kwargs):
        """
        Create a new test case.
        """
        try:
            data = json.loads(request.body)
            new_case = TestCase(name=data['name'], description=data['description'])
            new_case.save()
            return JsonResponse({'message': 'Test case created successfully.'}, status=201)
        except (json.JSONDecodeError, KeyError, ObjectDoesNotExist) as e:
            return JsonResponse({'error': str(e)}, status=400)


# URLs
urlpatterns = [
def path('test_report/', TestReportView.as_view(), name='test_report')\]
