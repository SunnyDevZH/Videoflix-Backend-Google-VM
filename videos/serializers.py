from rest_framework import serializers
from django.conf import settings
from .models import Video, Category
from .utils import generate_signed_url

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class VideoSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    thumbnail_url = serializers.SerializerMethodField()
    resolutions = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'description',
            'thumbnail_url',
            'video_file',  # Optional: Originaldatei
            'resolutions',  # Auflösungen als Dictionary
            'categories',
            'created_at'
        ]

    def get_signed_url(self, file_field):
        if not file_field:
            return ""
        if getattr(settings, "USE_GCS", False):
            return generate_signed_url(file_field.name)
        request = self.context.get("request")
        return request.build_absolute_uri(file_field.url) if request else file_field.url

    def get_thumbnail_url(self, obj):
        return self.get_signed_url(obj.thumbnail)

    def get_resolutions(self, obj):
        return {
            "360p": self.get_signed_url(obj.video_360p),
            "480p": self.get_signed_url(obj.video_480p),
            "720p": self.get_signed_url(obj.video_720p),
            "1080p": self.get_signed_url(obj.video_1080p),
        }
