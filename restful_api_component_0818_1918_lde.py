# 代码生成时间: 2025-08-18 19:18:21
from rest_framework import status, views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .models import UserProfile
from django.http import Http404
"""
A simple Django application component to create a RESTful API for user profiles.
"""

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user profile instances.
# NOTE: 重要实现细节
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        This view returns the list of profiles for the current logged in user.
# 改进用户体验
        """
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Create a new user profile instance.
        """
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        """
        Update the user profile instance.
        """
        serializer.save(user=self.request.user)
        
    def destroy(self, request, *args, **kwargs):
        """
        Destroy the user profile instance.
        If the profile does not belong to the current user, return a 403 Forbidden response.
        """
        try:
# 增强安全性
            obj = self.get_queryset().get(**kwargs)
            if obj.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
# 扩展功能模块
            self.perform_destroy(obj)
        except UserProfile.DoesNotExist:
            raise Http404
# 增强安全性
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# Define the URL patterns for the viewset
from django.urls import path, include
# 扩展功能模块
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# Define the models for the application
from django.db import models
# NOTE: 重要实现细节

class UserProfile(models.Model):
    """
    A user profile model.
# NOTE: 重要实现细节
    """
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
# FIXME: 处理边界情况
    
    def __str__(self):
        return self.user.username
    
# Define the serializers for the application
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """
    A serializer for the user profile model.
    """
# 添加错误处理
    class Meta:
        model = UserProfile
        fields = ['date_of_birth']
