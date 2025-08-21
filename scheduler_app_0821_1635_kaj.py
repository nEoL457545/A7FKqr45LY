# 代码生成时间: 2025-08-21 16:35:02
from django.apps import AppConfig
from django.db import models
from django.utils import timezone
from django.core.management import call_command
from django.urls import path
from celery import Celery

# 定义定时任务调度器模型
class ScheduledTask(models.Model):
    """
    定时任务模型
    """
    name = models.CharField(max_length=100, help_text="任务名称")
    schedule_type = models.CharField(max_length=50, choices=[
        ("interval", "时间间隔"),
        ("cron", "CRON表达式")], help_text="调度类型")
    schedule_value = models.CharField(max_length=200, help_text="调度值")
    command = models.CharField(max_length=200, help_text="要执行的命令")
    last_run_time = models.DateTimeField(null=True, blank=True, help_text="上次运行时间")
    created_at = models.DateTimeField(auto_now_add=True, help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, help_text="更新时间")

    def __str__(self):
        return self.name

# 定义定时任务调度器Celery配置
app = Celery('scheduler')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: None)

# 定义定时任务调度器任务
@app.task
def run_scheduled_task(task_id):
    """
    执行定时任务
    """
    try:
        task = ScheduledTask.objects.get(pk=task_id)
        if task.schedule_type == "cron":
            call_command(task.command)
        elif task.schedule_type == "interval":
            # 这里可以添加基于时间间隔的任务调度逻辑
            pass
        task.last_run_time = timezone.now()
        task.save()
    except ScheduledTask.DoesNotExist:
        # 任务不存在时的处理逻辑
        pass

# 定义定时任务调度器视图
from django.http import JsonResponse
from django.views import View

class ScheduledTaskView(View):
    """
    定时任务调度器视图
    """
    def get(self, request):
        """
        获取所有定时任务
        """
        tasks = ScheduledTask.objects.all()
        return JsonResponse(list(tasks.values()), safe=False)

    def post(self, request):
        """
        创建新的定时任务
        """
        # 这里可以添加创建新任务的逻辑
        pass

# 定义定时任务调度器路由
urlpatterns = [
    path('scheduled-task/', ScheduledTaskView.as_view(), name='scheduled-task'),
]

# 定时任务调度器配置类
class SchedulerAppConfig(AppConfig):
    """
    定时任务调度器配置类
    """
    name = 'scheduler'
    verbose_name = '定时任务调度器'