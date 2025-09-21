# 代码生成时间: 2025-09-21 08:29:58
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.views import View
from PIL import Image
import os

# models.py
def validate_image(file):
    """
    Validates that the uploaded file is an image.
    :param file: Uploaded file to validate.
    :raises ValidationError: If the file is not an image.
    """
    if not file.name.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')):
        raise ValidationError('%s is not a supported image format.' % file.name)

class ImageModel(models.Model):
    """
    A model for storing images.
    """
    image = models.ImageField(upload_to='images/', validators=[validate_image])
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    def __str__(self):
        return self.image.name

# views.py"