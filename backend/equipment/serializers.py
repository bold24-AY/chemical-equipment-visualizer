from rest_framework import serializers
from .models import Dataset


class DatasetSerializer(serializers.ModelSerializer):
    """
    Serializer for Dataset model.
    """
    class Meta:
        model = Dataset
        fields = ['id', 'uploaded_at', 'file_name', 'summary', 'raw_data']
        read_only_fields = ['id', 'uploaded_at']


class DatasetSummarySerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for dataset summaries (excludes raw data).
    """
    class Meta:
        model = Dataset
        fields = ['id', 'uploaded_at', 'file_name', 'summary']
        read_only_fields = ['id', 'uploaded_at']
