# 代码生成时间: 2025-08-23 03:09:33
# theme_switcher_app/views.py
"""
View functions for theme switcher application.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpRequest, HttpResponse

from .models import Theme
from .forms import ThemeForm

@login_required
def switch_theme(request: HttpRequest) -> HttpResponse:
    """
    Switches the theme for the currently logged in user.
    
    Args:
        request (HttpRequest): The current HTTP request.
        
    Returns:
        HttpResponse: Redirects to the home page after switching themes.
    """
    # Get the user's current theme
    current_theme = request.session.get('theme', 'default')
    
    # Get the available themes
    themes = Theme.objects.all()
    
    # Find the next theme in the sequence
    next_theme = None
    for theme in themes:
        if theme.name == current_theme:
            break
    if next_theme is None or theme == themes.last():
        next_theme = themes.first()
    else:
        next_theme = theme.get_next()
    
    # Update the user's session with the new theme
    request.session['theme'] = next_theme.name
    
    # Show a success message
    messages.success(request, f'Theme switched to {next_theme.name}')
    
    # Redirect to the home page
    return redirect(reverse('home'))


# theme_switcher_app/models.py
"""
Models for theme switcher application.
"""
from django.db import models

class Theme(models.Model):
    """
    Represents a theme.
    
    Attributes:
        name (str): The name of the theme.
    """
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

    def get_next(self):
        """
        Returns the next theme in the sequence.
        
        Returns:
            Theme: The next theme.
        """
        return Theme.objects.filter(name__gt=self.name).order_by('name').first()


# theme_switcher_app/urls.py
"""
URL configurations for theme switcher application.
"""
from django.urls import path
from . import views

app_name = 'theme_switcher'

urlpatterns = [
    path('switch/', views.switch_theme, name='switch_theme'),
]


# theme_switcher_app/forms.py
"""
Forms for theme switcher application.
"""
from django import forms

class ThemeForm(forms.Form):
    """
    A form for selecting a theme.
    
    Attributes:
        theme (ChoiceField): A dropdown menu for selecting a theme.
    """
    theme = forms.ChoiceField(choices=[(theme.name, theme.name) for theme in Theme.objects.all()])


# theme_switcher_app/admin.py
"""
Admin configurations for theme switcher application.
"""
from django.contrib import admin
from .models import Theme

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    

# Add the Theme model to your app's admin.py
# theme_switcher_app/apps.py
"""
Application configuration for theme switcher application.
"""
from django.apps import AppConfig

class ThemeSwitcherConfig(AppConfig):
    name = 'theme_switcher_app'
    verbose_name = 'Theme Switcher'