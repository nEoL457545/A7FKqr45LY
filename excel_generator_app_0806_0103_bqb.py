# 代码生成时间: 2025-08-06 01:03:40
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from django.views import View
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side
import io


# Models
class ExcelModel(models.Model):
    """
    A model for storing data that will be used to generate Excel files.
    """
    name = models.CharField(max_length=255)
    data = models.TextField()

    def __str__(self):
        return self.name



# Views
class ExcelView(View):
    """
    A view to generate and serve an Excel file.
    """
    def get(self, request, *args, **kwargs):
        try:
            data = ExcelModel.objects.all().values()
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
            wb = Workbook()
            ws = wb.active
            ws.title = 'Data'

            # Headers
            ws.append(['Name', 'Data'])

            # Data
            for item in data:
                ws.append([item['name'], item['data']])

            # Formatting
            for row in ws.iter_rows(min_row=1, max_col=2, max_row=2):
                for cell in row:
                    cell.font = Font(bold=True)
                    cell.alignment = Alignment(horizontal='center')
                    cell.border = Border(left=Side(style='thin'),
                                         right=Side(style='thin'),
                                         top=Side(style='thin'),
                                         bottom=Side(style='thin'))
            
            # Write data to output stream
            out = io.BytesIO()
            wb.save(out)
            out.seek(0)
            response.write(out.read())
            return response
        except Exception as e:
            return HttpResponse("An error occurred: " + str(e), status=500)


# URLs
urlpatterns = [
    path('generate_excel/', ExcelView.as_view(), name='generate_excel'),
]
