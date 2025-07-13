from django.contrib import admin
from .models import Video, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'thumbnail',
        'video_file',  # Das ist das Original-Upload
        'video_720p_preview',  # Custom Methode unten
        'created_at',
    )
    list_filter = ('categories', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    filter_horizontal = ('categories',)

    # Custom-Methode für Admin-Anzeige (optional)
    def video_720p_preview(self, obj):
        if obj.video_720p:
            return obj.video_720p.url
        return "Keine 720p-Datei vorhanden"

    video_720p_preview.short_description = "Video 720p URL"
