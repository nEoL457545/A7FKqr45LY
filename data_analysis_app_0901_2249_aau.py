# 代码生成时间: 2025-09-01 22:49:32
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import pandas as pd
import numpy as np
import json
from io import StringIO

# 数据分析模型
class DataAnalysis(models.Model):
    """
    模型用于存储数据和进行基本的统计分析。
    """
    # 数据字段
    data = models.TextField("数据", help_text="数据以CSV格式存储")
    
    def __str__(self):
        return "DataAnalysis: {}".format(self.data)

    # 计算基本统计信息
    def calculate_stats(self):
        """
        计算数据的基本统计信息。
        """
        # 将数据字段从字符串转换为DataFrame
        data_frame = pd.read_csv(StringIO(self.data))
        stats = {
            "mean": data_frame.mean().to_dict(),
            "std": data_frame.std().to_dict(),
            "min": data_frame.min().to_dict(),
            "max": data_frame.max().to_dict()
        }
        return stats

# 数据分析视图
class DataAnalysisView(View):
    """
    视图处理数据分析请求。
    """
    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """
        处理POST请求，接收数据，存储，并返回统计信息。
        """
        try:
            # 获取请求中的JSON数据
            data = json.loads(request.body)
            # 存储数据到数据库
            analysis = DataAnalysis.objects.create(data=data['data'])
            # 计算统计信息
            stats = analysis.calculate_stats()
            return JsonResponse(stats, safe=False)
        except Exception as e:
            # 错误处理
            return JsonResponse({'error': str(e)}, status=400)

# URL配置
data_analysis_urls = [
    path('analyze/', DataAnalysisView.as_view(), name='data_analysis'),
]

# 视图和URLs注册到Django
# 在Django项目的urls.py中添加以下代码：
# from django.urls import include, path
# from . import data_analysis_app
# ...
# url_patterns = [
#     ...
#     path('data_analysis/', include(data_analysis_app.urls)),
# ]