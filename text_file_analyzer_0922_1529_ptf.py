# 代码生成时间: 2025-09-22 15:29:55
import os
from django.core.exceptions import ValidationError
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.utils.deconstruct import deconstructible
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string

nltk.download('punkt')
nltk.download('stopwords')

"""Text File Analyzer Django Application"""

# Define models for storing text file analysis results
class TextAnalysisResult(models.Model):
    file_name = models.CharField(max_length=255)
    text_content = models.TextField()
    number_of_sentences = models.IntegerField()
    number_of_words = models.IntegerField()
    most_common_words = models.JSONField()

    def __str__(self):
        return f'Analysis of {self.file_name}'

    class Meta:
        verbose_name = 'Text Analysis Result'
        verbose_name_plural = 'Text Analysis Results'

"""Views for uploading text files and processing text content"""
class TextFileUploadView(View):
    def post(self, request, *args, **kwargs):
        "