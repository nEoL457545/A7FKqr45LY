# 代码生成时间: 2025-08-20 16:43:30
# shopping_cart_app.py

"""
This Django app provides a shopping cart feature.
"""

from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

# Models
class Product(models.Model):
    """Model to store product information."""
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    """Model to store shopping cart details."""
    items = models.ManyToManyField(Product)
    
    def __str__(self):
        return f"Cart with {self.items.count()} items"

class CartItem(models.Model):
    """Model to store individual items in the shopping cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

# Views
@csrf_exempt  # For simplicity, assuming CSRF tokens are handled elsewhere
@require_http_methods(['POST'])
def add_to_cart(request):
    """
    Adds a product to the shopping cart.
    :param request: HttpRequest object containing the product_id and quantity.
    :return: JsonResponse with success or error message.
    """
    try:
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = Product.objects.get(id=product_id)
        cart_id = request.session.get('cart_id')
        if not cart_id:
            cart = Cart()
            cart.save()
            request.session['cart_id'] = cart.id
        else:
            cart = Cart.objects.get(id=cart_id)
        CartItem.objects.update_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': CartItem.objects.get(cart=cart, product=product).quantity + quantity}
        )
        return JsonResponse({'message': 'Product added to cart successfully.'})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product does not exist.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(['GET'])
def view_cart(request):
    """
    Retrieves the contents of the shopping cart.
    :param request: HttpRequest object.
    :return: JsonResponse with the cart contents.
    """
    try:
        cart_id = request.session.get('cart_id')
        if not cart_id:
            return JsonResponse({'error': 'No cart found.'}, status=404)
        cart = Cart.objects.get(id=cart_id)
        items = CartItem.objects.filter(cart=cart)
        cart_contents = [{'product_name': item.product.name, 'quantity': item.quantity} for item in items]
        return JsonResponse({'cart_contents': cart_contents})
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'No cart found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# URLs
urlpatterns = [
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('view_cart/', view_cart, name='view_cart'),
]
