from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
    AllowAny,
)
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
from django_rq import get_queue

from .models import Video, Category
from .serializers import VideoSerializer, CategorySerializer
from .utils import generate_signed_url
from .tasks import generate_resolutions  # Dein Hintergrundjob


def get_video_url(video):
    if video.video_file:
        if getattr(settings, "USE_GCS", False):
            return generate_signed_url(video.video_file.name)
        else:
            return video.video_file.url
    return ''


class VideoListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data)


class VideoDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found'}, status=404)
        
        serializer = VideoSerializer(video, context={'request': request})
        return Response(serializer.data)


class CategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class VideoUploadView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.save()

            # Hintergrundjob starten, um Video in Auflösungen zu konvertieren
            queue = get_queue('default')
            queue.enqueue(generate_resolutions, video.id)

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_signed_video_url(request, filename):
    if getattr(settings, "USE_GCS", False):
        blob_name = f"videos/{filename}"
        try:
            url = generate_signed_url(blob_name)
            return Response({"url": url})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    else:
        url = settings.MEDIA_URL + 'videos/' + filename
        return Response({"url": url})
