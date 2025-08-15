# 代码生成时间: 2025-08-15 13:51:48
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

# Models
class MathToolModel(models.Model):
    """
    Database model for MathTool.
    Currently, there's no requirement for database storage, so this is just a placeholder.
    """
    pass

# Views
@method_decorator(csrf_exempt, name='dispatch')
class MathCalculationView(View):
    """
    A view to handle math operations like add, subtract, multiply, and divide.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for math operations.
        """
        try:
            data = request.POST.dict()
            operation = data.get('operation')
            if operation not in ['add', 'subtract', 'multiply', 'divide']:
                raise ValidationError('Invalid operation')
            
            # Get the numbers
            num1 = float(data.get('num1'))
            num2 = float(data.get('num2'))
            
            # Perform the operation
            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                if num2 == 0:
                    raise ValidationError('Cannot divide by zero')
                result = num1 / num2
            
            return JsonResponse({'result': result})
        except (ValueError, ZeroDivisionError, ValidationError) as e:
            return JsonResponse({'error': str(e)}, status=400)

# URLs
urlpatterns = [
    path('math/', MathCalculationView.as_view(), name='math_operation'),
]
