# 代码生成时间: 2025-09-05 16:42:25
from django.db import models
# FIXME: 处理边界情况
from django.shortcuts import render, redirect
from django.urls import path
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.db import transaction
import json

# Models
class Product(models.Model):
    """
    A model representing a product.
    """
# FIXME: 处理边界情况
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Cart(models.Model):
# 添加错误处理
    """
    A model representing a shopping cart.
    """
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    """
# 扩展功能模块
    A model representing an item in a shopping cart.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
# 添加错误处理
        return f"{self.quantity} of {self.product.name}"

# Views
@method_decorator(login_required, name='dispatch')
class CartView(LoginRequiredMixin, View):
    """
    View for handling shopping cart functionality.
    """
    def get(self, request):
        """
        Displays the shopping cart.
        """
        cart = Cart.objects.get(user=request.user)
        items = cart.product_set.annotate(total_price=Sum('cartitem__price')).all()
        return render(request, 'cart.html', {'items': items})

    def post(self, request):
        """
        Handles adding a product to the cart.
        """
        product_id = request.POST.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
# NOTE: 重要实现细节
            cart = Cart.objects.get(user=request.user)
            with transaction.atomic():
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                if not created:
                    cart_item.quantity += 1
                cart_item.save()
            return JsonResponse({'status': 'success'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

    def delete(self, request):
        """
        Handles removing a product from the cart.
        """
# 优化算法效率
        product_id = request.POST.get('product_id')
# 增强安全性
        try:
            cart = Cart.objects.get(user=request.user)
# 扩展功能模块
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
# FIXME: 处理边界情况
                cart_item.delete()
            return JsonResponse({'status': 'success'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product or cart item not found'}, status=404)

# URLs
urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
]
# 优化算法效率
