# 代码生成时间: 2025-09-20 17:07:01
import json
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

"""
Integration tests for the Django application.
This file contains tests for the application's main functionality using Django's test framework.
"""

class IntegrationTests(TestCase):
    """
    A test class for the integration tests of the application.
    """
    def setUp(self):
        """
        Set up the test client and test data.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_user_authenticated_access(self):
        """
        Test that an authenticated user can access a protected endpoint.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('protected-view'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_unauthenticated_access(self):
        """
        Test that an unauthenticated user cannot access a protected endpoint.
        """
        response = self.client.get(reverse('protected-view'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_model_instance_creation(self):
        """
        Test that a model instance can be created using the API.
        """
        data = {'name': 'Test Model', 'value': 42}
        response = self.client.post(reverse('model-create'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_response(self):
        """
        Test that a view returns the expected response.
        """
        response = self.client.get(reverse('test-view'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Hello, World!'})

    def test_error_handling(self):
        """
        Test that the application handles errors correctly.
        """
        response = self.client.get(reverse('error-view'))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
