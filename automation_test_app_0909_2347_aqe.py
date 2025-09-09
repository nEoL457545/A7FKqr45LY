# 代码生成时间: 2025-09-09 23:47:34
from django.apps import AppConfig
from django.db import models
from django.urls import path
from django.http import HttpResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

"""
自动化测试套件应用配置类
"""
class AutomationTestConfig(AppConfig):
    name = 'automation_test'
    verbose_name = 'Automation Test Suite'

"""
自动化测试模型
"""
class TestModel(models.Model):
    name = models.CharField(max_length=255, help_text='Test name')
    description = models.TextField(help_text='Test description')

    def __str__(self):
        return self.name

"""
自动化测试视图
"""
class TestView(View):
    def get(self, request, *args, **kwargs):
        try:
            tests = TestModel.objects.all()
            test_list = [{'name': test.name, 'description': test.description} for test in tests]
            return HttpResponse(
                json.dumps(test_list),
                content_type='application/json'
            )
        except ObjectDoesNotExist:
            return HttpResponse(
                json.dumps({'error': 'No tests found'}),
                content_type='application/json',
                status=404
            )

"""
自动化测试URL配置
"""
urlpatterns = [
    path('tests/', TestView.as_view(), name='test-list'),
]
