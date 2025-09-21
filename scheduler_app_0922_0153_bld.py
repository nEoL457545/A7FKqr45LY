# 代码生成时间: 2025-09-22 01:53:02
from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django_celery_beat.models import (
    PeriodicTask,
    CrontabSchedule,
    IntervalSchedule,
    TaskState
)
from datetime import datetime
import pytz

# 定时任务调度器模型
class ScheduledTask(models.Model):
    """ 数据库模型，用于存储定时任务信息 """
    task_name = models.CharField(max_length=255, unique=True)
    task_schedule = models.CharField(max_length=255)
    task_function = models.CharField(max_length=255)
    
    def __str__(self):
        return self.task_name

    class Meta:
        verbose_name = 'Scheduled Task'
        verbose_name_plural = 'Scheduled Tasks'

# 定时任务调度器视图
@require_http_methods(['GET', 'POST'])
def schedule_task(request):
    """
    处理定时任务调度请求
    
    Args:
        request (HttpRequest): HTTP请求对象
    
    Returns:
        JsonResponse: JSON格式的响应
    """
    if request.method == 'POST':
        try:
            task_name = request.POST.get('task_name')
            task_schedule = request.POST.get('task_schedule')
            task_function = request.POST.get('task_function')
            
            # 检查定时任务是否存在
            task, created = ScheduledTask.objects.get_or_create(
                task_name=task_name,
                task_schedule=task_schedule,
                task_function=task_function
            )
            
            # 创建或更新定时任务
            if created:
                task.save()
                message = f'Task {task_name} created successfully.'
            else:
                message = f'Task {task_name} updated successfully.'
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        try:
            tasks = ScheduledTask.objects.all()
            tasks_data = [
                {'task_name': task.task_name,
                 'task_schedule': task.task_schedule,
                 'task_function': task.task_function}
                for task in tasks
            ]
            return JsonResponse({'tasks': tasks_data}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'No tasks found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# 定时任务调度器URL配置
urlpatterns = [
    path('schedule/', schedule_task, name='schedule_task')
]