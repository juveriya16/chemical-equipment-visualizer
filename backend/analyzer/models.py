from django.db import models

# Create your models here.
from django.db import models

class Dataset(models.Model):
    filename = models.CharField(max_length=200)
    summary = models.JSONField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

class UploadHistory(models.Model):
    filename = models.CharField(max_length=255)
    total_count = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} ({self.uploaded_at})"

