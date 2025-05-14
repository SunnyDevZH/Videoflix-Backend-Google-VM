from django.contrib import admin
from .models import Video, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Zeigt ID und Name in der Liste an
    search_fields = ('name',)  # Ermöglicht die Suche nach Kategorien
    ordering = ('name',)  # Sortiert die Kategorien alphabetisch

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at')  # Zeigt wichtige Felder in der Liste an
    list_filter = ('category', 'created_at')  # Filter nach Kategorie und Erstellungsdatum
    search_fields = ('title', 'description')  # Ermöglicht die Suche nach Titel und Beschreibung
    ordering = ('-created_at',)  # Sortiert Videos nach Erstellungsdatum (neueste zuerst)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'thumbnail', 'video_url', 'category')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',),  # Klappt den Abschnitt ein
        }),
    )
    readonly_fields = ('created_at',)  # Macht das Erstellungsdatum schreibgeschützt
