from rest_framework import serializers
from django.conf import settings
from .models import Video, Category
from .utils import generate_signed_url

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    - Serializes the id and name fields of a category.
    """

    class Meta:
        model = Category
        fields = ['id', 'name']

class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Video model.
    - Serializes video details, including title, description, thumbnail, original file, available resolutions, categories, and creation date.
    - Provides signed URLs for video files and thumbnails, supporting both local and Google Cloud Storage.
    - Includes nested categories and dynamically generated resolution URLs.
    """
    categories = CategorySerializer(many=True, read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    resolutions = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'description',
            'thumbnail_url',
            'video_file',  # Originalvideo (Cloud-URL)
            'resolutions',  # URLs der verschiedenen Auflösungen
            'categories',
            'created_at',
        ]

    def get_signed_url(self, url):
        """
        Returns the URL for the given field.
        If you need signed URLs for GCS, implement generate_signed_url(url).
        """
        if not url:
            return ""
        # Falls du signierte URLs brauchst, hier anpassen:
        # if getattr(settings, "USE_GCS", False):
        #     return generate_signed_url(url)
        return url

    def get_thumbnail_url(self, obj):
        """
        Returns a signed URL for the video's thumbnail image.
        """
        # thumbnail ist weiterhin ein ImageField, daher wie gehabt:
        if obj.thumbnail:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
            return obj.thumbnail.url
        return ""

    def get_resolutions(self, obj):
        """
        Returns a dictionary of signed URLs for each available video resolution.
        """
        # Die Video-Felder sind jetzt Strings (Cloud-URLs)
        return {
            "360p": self.get_signed_url(obj.video_360p),
            "480p": self.get_signed_url(obj.video_480p),
            "720p": self.get_signed_url(obj.video_720p),
            "1080p": self.get_signed_url(obj.video_1080p),
        }
