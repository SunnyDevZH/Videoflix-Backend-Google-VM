# videos/serializers.py
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
    video_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'description',
            'thumbnail_url',
            'video_url',
            'video_file',
            'categories',
            'created_at'
        ]

    def get_video_url(self, obj):
        if not obj.video_file:
            return ""

        if getattr(settings, "USE_GCS", False):
            return generate_signed_url(obj.video_file.name)
        else:
            request = self.context.get("request")
            if request is not None:
                return request.build_absolute_uri(obj.video_file.url)
            return obj.video_file.url

    def get_thumbnail_url(self, obj):
        if not obj.thumbnail:
            return ""

        if getattr(settings, "USE_GCS", False):
            return generate_signed_url(obj.thumbnail.name)
        else:
            request = self.context.get("request")
            if request is not None:
                return request.build_absolute_uri(obj.thumbnail.url)
            return obj.thumbnail.url
