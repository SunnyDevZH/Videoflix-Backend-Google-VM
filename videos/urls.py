from django.urls import path
from .views import VideoListView, VideoDetailView, CategoryListView, VideoUploadView

urlpatterns = [
    path('', VideoListView.as_view(), name='video-list'),
    path('<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('upload/', VideoUploadView.as_view(), name='video-upload'),
]