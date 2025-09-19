# 代码生成时间: 2025-09-19 20:33:31
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic import View

# Define a model for storing user theme preferences
class Theme(models.Model):
    """
    Model to store user preferred themes.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Create views for theme switching
class ThemeView(View):
    """
    View for handling theme switching functionality.
    """

    @method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
    def get(self, request, *args, **kwargs):
        """
        GET method to display a form for theme selection.
        """
        # Retrieve available themes
        themes = Theme.objects.all()
        return render(request, 'theme_form.html', {'themes': themes})

    def post(self, request, *args, **kwargs):
        """
        POST method to handle theme selection and save user preference.
        """
        try:
            theme_name = request.POST.get('theme')
            theme = Theme.objects.get(name=theme_name)
            # Save the user's theme preference
            request.session['selected_theme'] = theme_name
            return HttpResponse('Theme changed to ' + theme_name)
        except Theme.DoesNotExist:
            raise Http404('Theme not found.')

# Define URLs for theme switching
from django.urls import path

urlpatterns = [
    path('theme/', ThemeView.as_view(), name='theme_switch'),
]

# Middleware to apply selected theme to templates
class ThemeMiddleware:
    """
    Middleware that applies the selected theme to the templates.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the selected theme from session
        selected_theme = request.session.get('selected_theme')
        if selected_theme:
            # Set the theme context processor to use the selected theme
            request.theme = selected_theme
        response = self.get_response(request)
        return response

# Add the middleware to settings.py
MIDDLEWARE = [
    ...
    'path.to.your.ThemeMiddleware',
]