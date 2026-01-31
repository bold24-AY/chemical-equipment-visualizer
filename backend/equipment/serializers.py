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


from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User registration.
    """
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
