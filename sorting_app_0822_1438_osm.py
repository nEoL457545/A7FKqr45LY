# 代码生成时间: 2025-08-22 14:38:56
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path

# Models
class Number(models.Model):
    """
    A model to store numbers for sorting.
    """
    number = models.IntegerField()

    def __str__(self):
        return str(self.number)

# Views
class SortView(View):
    """
    A view to handle sorting numbers.
    """
    def get(self, request, *args, **kwargs):
        """
        Return a JSON response with the sorted numbers.
        """
        numbers = Number.objects.all()
        sorted_numbers = self.sort_numbers(numbers)
        return JsonResponse({'sorted_numbers': sorted_numbers}, safe=False)

    def sort_numbers(self, numbers):
        """
        Sort the numbers using a simple sorting algorithm.
        """
        return sorted([num.number for num in numbers])

    def post(self, request, *args, **kwargs):
        """
        Create a new number instance from POST data.
        """
        try:
            number = request.POST.get('number')
            number_instance = Number(number=int(number))
            number_instance.save()
            return JsonResponse({'message': 'Number added successfully.'}, status=201)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid number'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# URLs
urlpatterns = [
    path('sort/', SortView.as_view(), name='sort'),
]
