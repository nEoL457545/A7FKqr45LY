# 代码生成时间: 2025-09-11 08:39:32
from django.db import models
from django.shortcuts import render, redirect
from django.urls import path
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from .forms import ProcessForm  # 假设有一个ProcessForm用于表单验证
import subprocess
import os
import signal
import sys

# Model to store process information
class Process(models.Model):
    """Model to represent a process."""
    name = models.CharField(max_length=100)
    command = models.CharField(max_length=255)
    status = models.CharField(max_length=10, default='stopped')
    
    def __str__(self):
        return self.name
    
    def start(self):
        """Start the process."""
        try:
            self.status = 'running'
            self.save()
            subprocess.Popen(self.command, shell=True)
        except Exception as e:
            # Log the exception and set status to stopped
            self.status = 'stopped'
            self.save()
            # Handle exception
            raise e
    
    def stop(self):
        """Stop the process."""
        try:
            # Find the process by command and kill it
            self.status = 'killed'
            self.save()
            subprocess.run(['pkill', '-f', self.command], check=True)
        except subprocess.CalledProcessError as e:
            # Log the exception and set status to stopped
            self.status = 'stopped'
            self.save()
            # Handle exception
            raise e
    
    # Add more process management methods as needed


# Views for process management
class ProcessListView(View):
    """View to display a list of processes."""
    def get(self, request, *args, **kwargs):
        """Return a list of processes."""
        processes = Process.objects.all()
        return render(request, 'process_list.html', {'processes': processes})

class ProcessCreateView(View):
    """View to create a new process."""
    form_class = ProcessForm
    template_name = 'process_form.html'
    
    def get(self, request, *args, **kwargs):
        """Return a new process creation form."""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        """Create a new process and start it."""
        form = self.form_class(request.POST)
        if form.is_valid():
            process = form.save()
            process.start()
            return redirect('process_list')
        return render(request, self.template_name, {'form': form})

class ProcessDetailView(View):
    """View to display a single process details."""
    def get(self, request, pk):
        """Return a single process details."""
        try:
            process = Process.objects.get(pk=pk)
            return render(request, 'process_detail.html', {'process': process})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Process not found'}, status=404)
    
    def put(self, request, pk):
        """Update a process."""
        try:
            process = Process.objects.get(pk=pk)
            form = ProcessForm(request.PUT, instance=process)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Process updated successfully'}, status=200)
            return JsonResponse({'error': 'Invalid process data'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Process not found'}, status=404)
    
    def delete(self, request, pk):
        """Delete a process."""
        try:
            process = Process.objects.get(pk=pk)
            process.delete()
            return JsonResponse({'message': 'Process deleted successfully'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Process not found'}, status=404)

class ProcessStartView(View):
    """View to start a process."""
    @require_http_methods(['POST'])
    def dispatch(self, request, pk):
        """Start a process."""
        try:
            process = Process.objects.get(pk=pk)
            process.start()
            return JsonResponse({'message': 'Process started successfully'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Process not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Failed to start process'}, status=500)
    
class ProcessStopView(View):
    """View to stop a process."""
    @require_http_methods(['POST'])
    def dispatch(self, request, pk):
        """Stop a process."""
        try:
            process = Process.objects.get(pk=pk)
            process.stop()
            return JsonResponse({'message': 'Process stopped successfully'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Process not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Failed to stop process'}, status=500)

# URLs for process management
urlpatterns = [
    path('processes/', ProcessListView.as_view(), name='process_list'),
    path('process/add/', ProcessCreateView.as_view(), name='process_add'),
    path('process/<pk>/', ProcessDetailView.as_view(), name='process_detail'),
    path('process/<pk>/start/', ProcessStartView.as_view(), name='process_start'),
    path('process/<pk>/stop/', ProcessStopView.as_view(), name='process_stop'),
]