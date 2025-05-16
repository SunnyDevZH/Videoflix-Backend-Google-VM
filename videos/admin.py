from django.contrib import admin
from .models import Video, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Zeigt ID und Name in der Liste an
    search_fields = ('name',)  # Ermöglicht die Suche nach Kategorien
    ordering = ('name',)  # Sortiert die Kategorien alphabetisch

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'thumbnail', 'video_url', 'video_file', 'created_at')  # Zeigt alle Felder an
    list_filter = ('categories', 'created_at')  # Filter für Kategorien und Erstellungsdatum
    search_fields = ('title', 'description')  # Ermöglicht die Suche nach Titel und Beschreibung
    readonly_fields = ('created_at',)  # Macht das Erstellungsdatum schreibgeschützt
    filter_horizontal = ('categories',)  # Ermöglicht eine bessere Auswahl von Kategorien
