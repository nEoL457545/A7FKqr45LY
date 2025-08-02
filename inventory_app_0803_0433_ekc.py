# 代码生成时间: 2025-08-03 04:33:13
from django.db import models
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# Models
class Item(models.Model):
    """Model for inventory items."""
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# Views
@method_decorator(csrf_exempt, name='dispatch')
class InventoryView(View):
    """View for handling inventory operations."""

    def get(self, request, *args, **kwargs):
        """Retrieve a list of all items in the inventory."""
        items = Item.objects.all()
        return JsonResponse(list(items.values('name', 'quantity', 'price')), safe=False)

    def post(self, request, *args, **kwargs):
        """Add a new item to the inventory."""
        name = request.POST.get('name')
        quantity = int(request.POST.get('quantity'))
        price = float(request.POST.get('price'))
        
        try:
            item = Item.objects.create(name=name, quantity=quantity, price=price)
            return JsonResponse({'id': item.id, 'name': item.name, 'quantity': item.quantity, 'price': item.price}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, pk, *args, **kwargs):
        """Update an existing item in the inventory."""
        item = Item.objects.get(pk=pk)
        name = request.POST.get('name')
        quantity = int(request.POST.get('quantity'))
        price = float(request.POST.get('price'))

        try:
            item.name = name
            item.quantity = quantity
            item.price = price
            item.save()
            return JsonResponse({'id': item.id, 'name': item.name, 'quantity': item.quantity, 'price': item.price})
        except Item.DoesNotExist:
            return HttpResponse(status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, pk, *args, **kwargs):
        """Remove an item from the inventory."""
        try:
            item = Item.objects.get(pk=pk)
            item.delete()
            return HttpResponse(status=204)
        except Item.DoesNotExist:
            return HttpResponse(status=404)

# URL Configuration
urlpatterns = [
    path('inventory/', InventoryView.as_view(), name='inventory'),
]
