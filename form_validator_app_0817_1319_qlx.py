# 代码生成时间: 2025-08-17 13:19:11
from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.http import HttpResponse
from django.views import View
from django.urls import path

# Models.py
class Contact(models.Model):
    """Model to store contact information."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

# Forms.py
class ContactForm(forms.ModelForm):
    """Form to validate contact data."""
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        """Custom validation for email field."""
        email = self.cleaned_data.get('email')
        if 'example.com' in email:
            raise ValidationError('Email cannot be from example.com')
        return email

# Views.py
class ContactFormView(View):
    """View to handle contact form submission."""
    def get(self, request):
        """Serve the contact form."""
        form = ContactForm()
        return HttpResponse(form)

    def post(self, request):
        """Process the contact form."""
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form instance and do something with it
            return HttpResponse('Form submitted successfully!')
        else:
            # Return the form with errors
            return HttpResponse(form.errors)

# Urls.py
urlpatterns = [
    path('contact/', ContactFormView.as_view(), name='contact_form'),
]
