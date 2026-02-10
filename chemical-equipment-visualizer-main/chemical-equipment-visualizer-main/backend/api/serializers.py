from rest_framework import serializers
from .models import Dataset
from django.contrib.auth.models import User

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'upload_date', 'data', 'summary']
        read_only_fields = ['upload_date']

class DatasetListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing datasets"""
    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'upload_date', 'summary']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']