# 代码生成时间: 2025-09-14 22:14:21
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import models
from django.views import View
from django.http import JsonResponse, HttpResponse, HttpRequest
from PIL import Image
from io import BytesIO

# Define the ImageResizer model
class ImageResizer(models.Model):
    """
    Model to store the image resizing requirements.
    """
    image = models.ImageField(upload_to='images/')  # Image field to store the image
    desired_size = models.CharField(max_length=10)  # Size in 'WIDTHxHEIGHT' format

    def __str__(self):
        return f"ImageResizer for {os.path.basename(self.image.name)}"

# Define the ImageResizerView
class ImageResizerView(View):
    """
    View to handle image resizing.
    """
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            # Get the uploaded image
            image_file = request.FILES.get('image')
            # Get the desired size from the request
            desired_size = request.POST.get('desired_size')

            # Check if the image file and desired size are provided
            if not image_file or not desired_size:
                return JsonResponse({'error': 'Image and desired size are required.'}, status=400)

            # Split the desired size into width and height
            width_str, height_str = desired_size.split('x')
            width = int(width_str)
            height = int(height_str)

            # Open the image and resize it
            with Image.open(image_file) as img:
                img = img.resize((width, height), Image.ANTIALIAS)
                resized_image = BytesIO()
                img.save(resized_image, format=img.format)
                resized_image.seek(0)

                # Save the resized image to the storage
                filename = os.path.basename(image_file.name)
                default_storage.save(f'resized/{filename}', ContentFile(resized_image.read()))

                # Return success response with the URL to the resized image
                resized_image_url = os.path.join(settings.MEDIA_URL, 'resized', filename)
                return JsonResponse({'resized_image_url': resized_image_url})

        except Exception as e:
            # Handle any exceptions
            return JsonResponse({'error': str(e)}, status=500)

# Define the ImageResizer URL pattern
from django.urls import path

urlpatterns = [
    path('resize/', ImageResizerView.as_view(), name='resize_image'),
]

