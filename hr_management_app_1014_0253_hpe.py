# 代码生成时间: 2025-10-14 02:53:21
from django.db import models
from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import View
from django.contrib.auth.decorators import login_required

# Creating a Django HR Management App

# Models
class Employee(models.Model):
    """Model representing an employee in the HR management system."""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}

# Views
class EmployeeListView(View):
    """View to display a list of employees."""
    def get(self, request):
        try:
            employees = Employee.objects.all()
            return render(request, 'employees/list.html', {'employees': employees})
        except Exception as e:
            return HttpResponse('Error: ' + str(e), status=500)

class EmployeeDetailView(View):
    """View to display a detailed view of an employee."""
    def get(self, request, employee_id):
        try:
            employee = Employee.objects.get(pk=employee_id)
            return render(request, 'employees/detail.html', {'employee': employee})
        except Employee.DoesNotExist:
            raise Http404('Employee does not exist')
        except Exception as e:
            return HttpResponse('Error: ' + str(e), status=500)

# URL Configurations
urlpatterns = [
d    path('employees/', login_required(EmployeeListView.as_view()), name='employee-list'),
    path('employees/<int:employee_id>/', login_required(EmployeeDetailView.as_view()), name='employee-detail')
]
