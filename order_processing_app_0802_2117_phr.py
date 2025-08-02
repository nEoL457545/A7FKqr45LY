# 代码生成时间: 2025-08-02 21:17:44
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import Order

# Define the Order model
class Order(models.Model):
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    customer_name = models.CharField(max_length=100)
    order_status = models.CharField(max_length=50, default='Pending')
    
    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
# Define the views
class OrderCreateView(View):
    """
    Create a new order.
    """
    def post(self, request):
        try:
            # Get data from request
            product_name = request.POST.get('product_name')
            quantity = request.POST.get('quantity')
            customer_name = request.POST.get('customer_name')
            quantity = int(quantity)  # Validate quantity as an integer
            
            # Create a new order instance
            order = Order(
                product_name=product_name,
                quantity=quantity,
                customer_name=customer_name
            )
            order.save()
            
            # Return a success response
            return JsonResponse({'message': 'Order created successfully'}, status=201)
        except (ValueError, ValidationError) as e:
            # Handle invalid data
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            # Handle any other exceptions
            return JsonResponse({'error': 'An error occurred'}, status=500)
    
    def get(self, request):
        # Get all orders (for demonstration purposes)
        orders = Order.objects.all()
        return render(request, 'orders/order_list.html', {'orders': orders})

# Define the URL patterns
urlpatterns = [
    # POST /orders to create a new order
    path('orders/', csrf_exempt(OrderCreateView.as_view()), name='order_create'),
    # GET /orders to view all orders
    path('orders/', OrderCreateView.as_view(), name='order_list'),
]

# Define the templates in templates/orders/order_list.html
# {% extends "base.html" %}
# {% block content %}
#     <h2>Order List</h2>
#     <ul>
#         {% for order in orders %}
#             <li>{{ order.product_name }} - {{ order.quantity }} - {{ order.customer_name }} - {{ order.order_status }}</li>
#         {% endfor %}
#     </ul>
# {% endblock %}
