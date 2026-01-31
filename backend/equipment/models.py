from django.db import models


class Dataset(models.Model):
    """
    Model to store uploaded equipment CSV datasets.
    Keeps only the last 5 uploads.
    """
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    summary = models.JSONField()  # Stores analytics: averages, counts, distributions
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    summary = models.JSONField()  # Stores analytics: averages, counts, distributions
    raw_data = models.JSONField()  # Stores the actual equipment records
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='datasets', null=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Equipment Dataset'
        verbose_name_plural = 'Equipment Datasets'
    
    def __str__(self):
        return f"{self.file_name} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
