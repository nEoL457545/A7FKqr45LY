# 代码生成时间: 2025-09-18 16:34:55
import os
from django.core.exceptions import ValidationError
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from io import StringIO
import csv

def setup_nltk_resources():
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

class TextAnalysis(models.Model):
    """储存文本分析结果的模型。"""
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'TextAnalysis {self.pk}'

class TextAnalysisView(View):
    """
    视图类，用于处理文本文件上传，并分析其内容。
    """
    def post(self, request, *args, **kwargs):
        """处理POST请求，分析上传的文本文件内容。"""
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No file provided.'}, status=400)

        try:
            text = file.read().decode('utf-8')
            analysis_result = analyze_text(text)
            return JsonResponse(analysis_result)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred.'}, status=500)

    def get(self, request, *args, **kwargs):
        """处理GET请求，返回分析结果示例。"""
        example_result = {
            'words_count': 123,
            'stop_words_count': 50,
            'lemmatized_words': ['example', 'lemmatized', 'words']
        }
        return JsonResponse(example_result)

def analyze_text(text):
    """
    分析文本内容，返回一个包含基本统计和词形还原的词列表的字典。
    """
    setup_nltk_resources()
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    words_count = len(words)
    stop_words_count = len([word for word in words if word.lower() in stop_words])
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return {
        'words_count': words_count,
        'stop_words_count': stop_words_count,
        'lemmatized_words': lemmatized_words
    }

# URL配置
urlpatterns = [
    path('analyze/', method_decorator(csrf_exempt, name='dispatch')(TextAnalysisView.as_view()), name='text_analysis'),
]
