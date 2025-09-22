# 代码生成时间: 2025-09-23 00:40:44
from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

# Models
class Product(models.Model):
    """Model representing a product in the inventory."""
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

# Views
class ProductListView(View):
    """View to list all products in the inventory."""
    def get(self, request):
        try:
            products = Product.objects.all()
            return JsonResponse(list(products.values()), safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'No products found.'}, status=404)

    def post(self, request):
        try:
            # Assuming request.POST has 'name', 'quantity', and 'price' fields
            new_product = Product.objects.create(
                name=request.POST.get('name'),
                quantity=int(request.POST.get('quantity')),
                price=float(request.POST.get('price'))
            )
            return JsonResponse({'id': new_product.id}, status=201)
        except ValueError:
            return JsonResponse({'error': 'Invalid data, please provide valid input.'}, status=400)

class ProductDetailView(View):
    """View to get, update, or delete a specific product."""
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            return JsonResponse(product.values())
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Product not found.'}, status=404)

    def put(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product.name = request.PUT.get('name', product.name)
            product.quantity = int(request.PUT.get('quantity', product.quantity))
            product.price = float(request.PUT.get('price', product.price))
            product.save()
            return JsonResponse(product.values())
        except ValueError:
            return JsonResponse({'error': 'Invalid data, please provide valid input.'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Product not found.'}, status=404)

    def delete(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return JsonResponse({'message': 'Product deleted successfully.'})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Product not found.'}, status=404)

# URLs
inventory_patterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
]

# Note: This is a simplified representation of a Django app component.
# For full functionality, you will need to create a Django project,
# include this app, and define the necessary Django settings.
# Also, ensure to handle forms, authentication, permissions, and other
# aspects of a robust Django application.