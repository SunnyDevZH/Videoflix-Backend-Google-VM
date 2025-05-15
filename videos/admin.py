from django.contrib import admin
from .models import Video, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Zeigt ID und Name in der Liste an
    search_fields = ('name',)  # Ermöglicht die Suche nach Kategorien
    ordering = ('name',)  # Sortiert die Kategorien alphabetisch

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_file')
