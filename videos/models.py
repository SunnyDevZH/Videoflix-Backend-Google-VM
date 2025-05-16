from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # Beschreibung optional
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)  # Optionales Thumbnail
    video_url = models.URLField(blank=True)  # z. B. Google Cloud Storage URL
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)  # Optionales Original-File
    categories = models.ManyToManyField(Category, blank=True)  # Mehrere Kategorien möglich
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
