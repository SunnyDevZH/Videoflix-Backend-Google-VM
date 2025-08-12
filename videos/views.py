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
import logging

from .models import Video, Category
from .serializers import VideoSerializer, CategorySerializer
from .utils import generate_signed_url
from .tasks import generate_resolutions  # Dein Hintergrundjob

logger = logging.getLogger(__name__)

def get_video_url(video):
    # Angepasst für URLField!
    if video.video_file:
        # Falls du signierte URLs für GCS brauchst, hier anpassen:
        # if getattr(settings, "USE_GCS", False):
        #     return generate_signed_url(video.video_file)
        return video.video_file
    return ''

class VideoListView(APIView):
    """
    Returns a list of all videos.
    - Accessible to authenticated users and read-only for unauthenticated users.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data)

class VideoDetailView(APIView):
    """
    Returns the details of a single video by its primary key.
    - Accessible to authenticated users and read-only for unauthenticated users.
    - Returns 404 if the video does not exist.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found'}, status=404)
        
        serializer = VideoSerializer(video, context={'request': request})
        return Response(serializer.data)

class CategoryListView(APIView):
    """
    Returns a list of all video categories.
    - Accessible to everyone.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class VideoUploadView(APIView):
    """
    Allows admin users to upload a new video.
    - Starts a background job to generate different video resolutions.
    - Returns job status and job ID in the response.
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.save()

            # Hintergrundjob starten, um Video in Auflösungen zu konvertieren
            queue = get_queue('default')
            job = queue.enqueue(generate_resolutions, video.id)
            
            logger.info(f"Task generate_resolutions für Video {video.id} enqueued mit Job-ID {job.id}")

            response_data = serializer.data.copy()
            response_data['task_job_id'] = job.id
            response_data['task_status'] = 'enqueued'

            return Response(response_data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_signed_video_url(request, filename):
    """
    Returns a signed URL for accessing a video file.
    - Uses Google Cloud Storage if enabled, otherwise returns a local media URL.
    """
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
