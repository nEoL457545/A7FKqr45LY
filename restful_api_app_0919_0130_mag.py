# 代码生成时间: 2025-09-19 01:30:26
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Models
class Book(models.Model):
    """ A simple Book model. """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    published_date = models.DateField()

    def __str__(self):
        return self.title

# Views
@method_decorator(csrf_exempt, name='dispatch')
class BookAPIView(View):
    """
    A simple RESTful API for interacting with Book objects.
    Provides GET and POST methods for the Book model.
    """

    def get(self, request):
        """
        Retrieves a list of all Book instances.
        """
        books = Book.objects.all()
        books_data = [{'title': book.title, 'author': book.author, 'isbn': book.isbn, 'published_date': book.published_date} for book in books]
        return JsonResponse({'books': books_data}, safe=False)

    def post(self, request):
        """
        Creates a new Book instance from JSON data.
        """
        data = request.POST
        new_book = Book(title=data['title'], author=data['author'], isbn=data['isbn'], published_date=data['published_date'])
        new_book.save()
        return JsonResponse({'message': 'Book created successfully!'}, status=201)

# URL Patterns
urlpatterns = [
    path('books/', BookAPIView.as_view()),
]
