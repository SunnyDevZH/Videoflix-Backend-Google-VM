from rest_framework import serializers
from .models import Video, Category
from .utils import generate_signed_url  # von utils importieren

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class VideoSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)  # Verwende das richtige Feld
    video_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'thumbnail', 'video_url', 'video_file', 'categories', 'created_at']

    def get_video_url(self, obj):
        if obj.video_file:
            return generate_signed_url(obj.video_file.name)
        return ""