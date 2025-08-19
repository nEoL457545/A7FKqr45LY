# 代码生成时间: 2025-08-19 17:48:20
from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import User

"""
This Django app component handles form data validation.
It includes models, views, and urls for demonstration purposes.
"""

# Models.py
class User(models.Model):
    """Model representing a user with a username and email."""
    username = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.username

# Forms.py
class UserForm(forms.ModelForm):
    """Form for user data."""
    class Meta:
        model = User
        fields = ['username', 'email']
        
    def clean_email(self):
        """
        Validate that the email is not already in use.
        If the email is taken, raise a ValidationError.
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use.')
        return email

# Views.py
class UserFormView(View):
    """View to handle user form submissions."""
    def get(self, request):
        """Serve the form page."""
        form = UserForm()
        return render(request, 'user_form.html', {'form': form})
        
    def post(self, request):
        """Handle the form submission and validate data."""
        form = UserForm(request.POST)
        if form.is_valid():
            # Save the new user and redirect to success page
            form.save()
            return HttpResponse('User created successfully.')
        else:
            # Return the form with errors
            return render(request, 'user_form.html', {'form': form})

# Urls.py
urlpatterns = [
    """URL patterns for the user form."""
    path('user_form/', UserFormView.as_view(), name='user_form'),
]
