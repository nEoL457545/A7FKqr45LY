# 代码生成时间: 2025-08-20 05:08:51
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from django_celery_beat.models import PeriodicTask, CrontabSchedule

# Initialize the Celery app
app = Celery('scheduled_tasks')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: None)

# Set up logging
logger = get_task_logger(__name__)

# Define a model to store task schedule
class ScheduledTask(models.Model):
    """
    A model to store scheduled tasks with their details.
    """
    name = models.CharField(max_length=100, unique=True, help_text="The name of the task.")
    interval = models.CharField(max_length=255, help_text="A crontab expression for the task schedule.")
    task = models.CharField(max_length=100, help_text="The name of the task function.")
    last_run_at = models.DateTimeField(null=True, blank=True, help_text="The last time the task ran.")
    
    def __str__(self):
        return f"{self.name} - {self.interval} - {self.task}"
    
# Define a Celery task
@app.task
def run_task(name):
    """
    A Celery task that will be run on schedule.
    """
    try:
        # Logic to perform task goes here
        logger.info(f"Task '{name}' started.")
        # Example: save a log or perform some action
        logger.info(f"Task '{name}' completed successfully.")
    except Exception as e:
        # Handle any exceptions that occur during the task
        logger.error(f"An error occurred while running task '{name}': {e}")
    
    finally:
        # Update last_run_at to current time after the task execution
        task = ScheduledTask.objects.get(name=name)
        task.last_run_at = timezone.now()
        task.save()


# Using Django-celery-beat to schedule tasks
@periodic_task(run_every=crontab(minute='*/5'), name='Example Task')
def example_task():
    """
    Example periodic task that runs every 5 minutes.
    """
    run_task('example_task')
    
# Add 'django_celery_beat' to your installed apps and include the following in your urls.py
# to set up the Django-celery-beat admin interface
# from django.urls import path
# from django_celery_beat import views as celery_views
# urlpatterns = [
#     path('celery/', include(celery_urls)),
# ]