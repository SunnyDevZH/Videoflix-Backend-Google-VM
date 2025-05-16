from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Video, Category
from .serializers import VideoSerializer, CategorySerializer

from google.cloud import storage
from datetime import timedelta
from django.conf import settings
from .utils import generate_signed_url

# 🔐 Hilfsfunktion für signierte URL
def generate_signed_url(blob_name, expiration_minutes=15):
    storage_client = storage.Client(credentials=settings.GS_CREDENTIALS)
    bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=expiration_minutes),
        method="GET",
    )

    return url


# 📺 Liste aller Videos
class VideoListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        videos = Video.objects.all()
        for video in videos:
            if video.video_file:  # wenn es ein FileField mit Pfad gibt
                video.video_url = generate_signed_url(video.video_file.name)
            else:
                video.video_url = ''
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data)

# 📺 Einzelnes Video
class VideoDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
            serializer = VideoSerializer(video)
            return Response(serializer.data)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found'}, status=404)


# 📁 Liste aller Kategorien
class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


# ⬆️ Video hochladen (nur Admins)
class VideoUploadView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# 🔐 Signierte URL abrufen für ein Video (nur eingeloggte Benutzer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_signed_video_url(request, filename):
    blob_name = f"videos/{filename}"  # falls deine Videos im Unterordner "videos/" liegen
    try:
        url = generate_signed_url(blob_name)
        return Response({"url": url})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
