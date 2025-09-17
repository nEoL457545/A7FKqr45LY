# 代码生成时间: 2025-09-17 13:53:29
# document_converter_app/__init__.py
# 这是一个Django应用的初始化文件，用于初始化文档转换器应用。

# document_converter_app/models.py
"""
Models for the document_converter_app app.
"""
from django.db import models

class Document(models.Model):
    """
    A model representing a document that can be converted.
    """
    title = models.CharField(max_length=255, help_text="The title of the document.")
    original_file = models.FileField(upload_to='documents/', help_text="The original document file.")
    converted_file = models.FileField(upload_to='converted_documents/', blank=True, null=True, help_text="The converted document file.")

    def __str__(self):
        return self.title

# document_converter_app/views.py
"""
Views for the document_converter_app app.
"""
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseNotAllowed
from .models import Document
from .forms import DocumentForm

import docx
import pdfrw
from docx import Document as WordDocument
from io import BytesIO

@require_http_methods(['GET', 'POST'])
def convert_document(request):
    """
    Converts a document from Word format to PDF format.
    """
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            try:
                # Convert the document
                convert_word_to_pdf(document)
                document.converted_file.name = f"{document.title}.pdf"
                document.save()
                return redirect('converted_document', document_id=document.id)
            except Exception as e:
                # Handle conversion errors
                return HttpResponse(f"An error occurred: {e}", status=500)
    else:
        form = DocumentForm()
    return render(request, 'document_converter_app/convert.html', {'form': form})

def convert_word_to_pdf(document):
    """
    Converts a word document to a PDF.
    """
    doc = docx.Document(document.original_file.path)
    output = BytesIO()
    pdfrw PdfWriter().addpage(doc).write(output)
    document.converted_file.save(document.title + ".pdf", ContentFile(output.getvalue()), save=False)

# document_converter_app/urls.py
"""
URLs for the document_converter_app app.
"""
from django.urls import path
from .views import convert_document

urlpatterns = [
    path('convert/', convert_document, name='convert_document'),
]

# document_converter_app/forms.py
"""
Forms for the document_converter_app app.
"""
from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    """
    A form for uploading and processing a document for conversion.
    """
    class Meta:
        model = Document
        fields = ['title', 'original_file']
