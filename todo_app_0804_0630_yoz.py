# 代码生成时间: 2025-08-04 06:30:23
from django.db import models
from django.urls import path
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.db.models import Q
import json

# 数据模型设计
class Todo(models.Model):
    """Todo 数据模型"""
    title = models.CharField(max_length=255, verbose_name="标题")
    description = models.TextField(verbose_name="描述")
    completed = models.BooleanField(default=False, verbose_name="完成")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "待办事项"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

# 视图
class TodoView(View):
    """Todo视图类"""

    def get(self, request, *args, **kwargs):
        "