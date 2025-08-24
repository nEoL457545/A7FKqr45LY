# 代码生成时间: 2025-08-24 16:33:37
from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.urls import path
from time import time
import requests
import threading

"""
A Django app component to perform performance testing.
It provides a simple API endpoint to simulate multiple requests to a given URL.
"""

class PerformanceTestModel(models.Model):
    """
    A simple model to store performance test results.
    """
    url = models.URLField(max_length=200, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.FloatField()
    status_code = models.IntegerField()

    def __str__(self):
        return self.url

class PerformanceTestView:
    "