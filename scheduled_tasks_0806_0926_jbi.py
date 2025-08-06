# 代码生成时间: 2025-08-06 09:26:28
import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.views import View
from celery import Celery, states
from celery.exceptions import SoftTimeLimitExceeded
from celery.result import AsyncResult
from celery.utils.log import get_task_logger

# Set the default Django settings module for the 'celery' program.
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('your_project')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


logger = get_task_logger(__name__)


def make_task(name, **kwargs):
    """
    Helper function for creating a Celery task.
    """
    return app.task(name, **kwargs)



class Task(models.Model):
    """
    Represents a scheduled task in the database.
    """
    name = models.CharField(max_length=255, help_text="The name of the task.")
    task_id = models.CharField(max_length=255, unique=True, blank=True, help_text="The task's unique ID.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the task was created.")
    last_run = models.DateTimeField(null=True, blank=True, help_text="When the task was last run.")
    result = models.JSONField(null=True, blank=True, help_text="The result of the task.")
    error = models.JSONField(null=True, blank=True, help_text="Any errors that occurred during the task.")
    status = models.CharField(max_length=50, choices=[(s, s) for s in states.STATES], default=states.PENDING, help_text="The status of the task.")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Scheduled Task"
        verbose_name_plural = "Scheduled Tasks"


@make_task
def run_task(self, task_id):
    """
    Runs a scheduled task.
    """
    try:
        task = Task.objects.get(task_id=task_id)
        # Perform the task's logic here. This is an example.
        result = {"message": "Task completed successfully."}
        task.result = result
        task.last_run = datetime.datetime.now()
        task.status = states.SUCCESS
        task.save()
    except Task.DoesNotExist:
        logger.error("Task does not exist.")
        return {"error": "Task does not exist."}
    except SoftTimeLimitExceeded:
        logger.error("Task exceeded the time limit.")
        return {"error": "Task exceeded the time limit."}
    except Exception as e:
        logger.error("An error occurred: %s