from rest_framework import serializers
from .models import Video, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class VideoSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'thumbnail', 'video_url', 'category', 'created_at']