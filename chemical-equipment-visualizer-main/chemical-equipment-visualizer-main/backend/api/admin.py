from django.contrib import admin
from .models import Dataset

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['id', 'filename', 'upload_date']
    list_filter = ['upload_date']
    search_fields = ['filename']