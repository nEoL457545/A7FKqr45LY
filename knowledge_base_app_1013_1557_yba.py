# 代码生成时间: 2025-10-13 15:57:52
import os
from django.db import models
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import path
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

# Models
class Article(models.Model):
    """Model representing an article in the knowledge base."""
    title = models.CharField(max_length=200, help_text="Enter a title for the article.")
    content = models.TextField(help_text="Enter the content of the article.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

# Views
class ArticleListView(LoginRequiredMixin, ListView):
    """View to display a list of all articles."""
    model = Article
    template_name = 'knowledge_base/article_list.html'
    context_object_name = 'articles'

class ArticleDetailView(LoginRequiredMixin, DetailView):
    """View to display a single article."""
    model = Article
    template_name = 'knowledge_base/article_detail.html'
    context_object_name = 'article'

class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """View to create a new article."""
    model = Article
    template_name = 'knowledge_base/article_form.html'
    fields = ['title', 'content']
    permission_required = 'knowledge_base.add_article'

    def form_valid(self, form):
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """View to update an existing article."""
    model = Article
    template_name = 'knowledge_base/article_form.html'
    fields = ['title', 'content']
    permission_required = 'knowledge_base.change_article'

    def form_valid(self, form):
        return super().form_valid(form)

class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """View to delete an existing article."""
    model = Article
    template_name = 'knowledge_base/article_confirm_delete.html'
    success_url = '/knowledge_base/'
    permission_required = 'knowledge_base.delete_article'

# URLs
app_name = 'knowledge_base'  # namespace for URL names
urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/new/', ArticleCreateView.as_view(), name='article_new'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]
