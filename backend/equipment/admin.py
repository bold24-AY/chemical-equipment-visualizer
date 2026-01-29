from django.contrib import admin
from .models import Dataset


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'uploaded_at', 'get_equipment_count']
    list_filter = ['uploaded_at']
    search_fields = ['file_name']
    readonly_fields = ['uploaded_at', 'summary', 'raw_data']
    
    def get_equipment_count(self, obj):
        return obj.summary.get('total_equipment', 0)
    get_equipment_count.short_description = 'Equipment Count'
