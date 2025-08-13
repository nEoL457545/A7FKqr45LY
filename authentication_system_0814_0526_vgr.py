# 代码生成时间: 2025-08-14 05:26:38
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.views import View

"""
User Login System View
Handles user login requests and authentication.
"""

@method_decorator(sensitive_post_parameters(), name='dispatch')
class UserLoginView(View):
    """
    A class-based view for handling user login.
    """
    @csrf_exempt
    @require_http_methods(['POST'])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        """
        Authenticate user credentials and log the user in.
        :param request: Request object containing credentials.
        :return: JSON response with authentication status.
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required.'}, status=400)
        
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User does not exist.'}, status=404)
        
        user_authenticated = authenticate(username=username, password=password)
        if user_authenticated:
            login(request, user)
            return JsonResponse({'message': 'User logged in successfully.'})
        else:
            return JsonResponse({'error': 'Invalid username or password.'}, status=401)


"""
User Login URL Configuration
"""
from django.urls import path
from .views import UserLoginView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
]

"""
User Login Models
"""
# Assuming the default Django User model is sufficient for this system.
# Additional fields or model modifications would be defined here.

