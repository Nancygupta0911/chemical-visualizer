from django.db import models
from django.contrib.auth.models import User
import json

class Dataset(models.Model):
    filename = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()  # Store the CSV data as JSON
    summary = models.JSONField()  # Store computed statistics
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return f"{self.filename} - {self.upload_date.strftime('%Y-%m-%d %H:%M')}"
    
    @classmethod
    def cleanup_old_datasets(cls):
        """Keep only the last 5 datasets"""
        datasets = cls.objects.all()
        if datasets.count() > 5:
            old_datasets = datasets[5:]
            for dataset in old_datasets:
                dataset.delete()