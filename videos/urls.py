from django.urls import path
from .views import (
    VideoListView, VideoDetailView, CategoryListView, 
    VideoUploadView, get_signed_video_url  # <== wichtig!
)

urlpatterns = [
    path('', VideoListView.as_view(), name='video-list'),
    path('<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('upload/', VideoUploadView.as_view(), name='video-upload'),
    
    # 📦 Signierte URL für Video holen (z. B. für <video src=...>)
    path('signed-url/<str:filename>/', get_signed_video_url, name='get-signed-url'),
]
