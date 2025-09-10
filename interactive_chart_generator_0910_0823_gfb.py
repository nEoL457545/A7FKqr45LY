# 代码生成时间: 2025-09-10 08:23:24
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import json
import numpy as np
import pandas as pd
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

# 定义模型
class ChartModel(models.Model):
    title = models.CharField(max_length=100)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # 添加数据
    def add_data(self, new_data):
        """
        Add new data to the chart's dataset.
        
        :param new_data: A dictionary containing the new data.
        """
        try:
            # 将新数据转换为DataFrame
            new_df = pd.DataFrame([new_data])
            # 合并数据
            self.data = self.data.append(new_df, ignore_index=True)
            # 保存到数据库
            self.save()
        except Exception as e:
            # 错误处理
            return JsonResponse({'error': str(e)}, status=500)

    # 获取数据
    def get_data(self):
        """
        Get the chart's dataset.
        
        :return: The chart's dataset as a JSON response.
        """
        try:
            # 转换为DataFrame
            df = pd.DataFrame(self.data)
            # 转换为JSON
            return JsonResponse({'data': df.to_json(orient='records')})
        except Exception as e:
            # 错误处理
            return JsonResponse({'error': str(e)}, status=500)


# 定义视图
class InteractiveChartView(View):
    def get(self, request, *args, **kwargs):
        try:
            # 获取图表数据
            chart = ChartModel.objects.get(id=kwargs.get('chart_id'))
            return chart.get_data()
        except ChartModel.DoesNotExist:
            return JsonResponse({'error': 'Chart not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request, *args, **kwargs):
        try:
            # 获取图表ID
            chart_id = kwargs.get('chart_id')
            # 解析请求体数据
            data = json.loads(request.body)
            # 获取或创建图表实例
            chart = ChartModel.objects.get_or_create(id=chart_id)[0]
            # 添加数据到图表
            return chart.add_data(data)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Chart not found'}, status=404)
        except IntegrityError:
            return JsonResponse({'error': 'Integrity error'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# 定义urls
urlpatterns = [
    path('chart/<str:chart_id>/', InteractiveChartView.as_view(), name='interactive_chart'),
]
