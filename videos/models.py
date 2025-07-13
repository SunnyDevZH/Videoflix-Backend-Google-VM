from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    video_file = models.FileField(upload_to='videos/original/', null=True, blank=True)

    # Neue Felder für verschiedene Auflösungen
    video_360p = models.FileField(upload_to='videos/360p/', null=True, blank=True)
    video_480p = models.FileField(upload_to='videos/480p/', null=True, blank=True)
    video_720p = models.FileField(upload_to='videos/720p/', null=True, blank=True)
    video_1080p = models.FileField(upload_to='videos/1080p/', null=True, blank=True)

    categories = models.ManyToManyField(Category, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
