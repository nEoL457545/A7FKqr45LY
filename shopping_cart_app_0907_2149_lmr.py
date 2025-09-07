# 代码生成时间: 2025-09-07 21:49:13
# shopping_cart_app.py
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse

# Models
# TODO: 优化性能
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
# 改进用户体验
    
    def __str__(self):
        return f"{self.user.username}'s Cart"

    def add_product(self, product_id, quantity):
        product = get_object_or_404(Product, pk=product_id)
        self.products.add(product, through_defaults={'quantity': quantity})
    
    def remove_product(self, product_id):
        product = get_object_or_404(Product, pk=product_id)
        self.products.remove(product)

    def total_price(self):
        from django.db.models import Sum
        return self.products.aggregate(total=Sum('product__price' * F('quantity')))['total'] or 0

# Views
from django.db.models import F
# 扩展功能模块

def cart(request):
    if request.method == 'GET':
        cart = Cart.objects.get(user=request.user)
        products = cart.products.all()
# 改进用户体验
        total = cart.total_price()
        return render(request, 'cart.html', {'products': products, 'total': total})
    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
# 优化算法效率
            product_id = request.POST.get('product_id')
# 添加错误处理
            quantity = int(request.POST.get('quantity', 1))
            cart = Cart.objects.get(user=request.user)
            cart.add_product(product_id, quantity)
        elif action == 'remove':
            product_id = request.POST.get('product_id')
            cart = Cart.objects.get(user=request.user)
            cart.remove_product(product_id)
        return JsonResponse({'status': 'success'})
# NOTE: 重要实现细节

# URLs
from django.urls import path

urlpatterns = [
# NOTE: 重要实现细节
    path('cart/', views.cart, name='cart'),
]
