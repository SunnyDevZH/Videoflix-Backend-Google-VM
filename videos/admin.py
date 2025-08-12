from django.contrib import admin
from django.utils.html import format_html
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
        'video_file',         
        'video_file_url',     
        'video_720p_preview', 
        'created_at',
    )
    list_filter = ('categories', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'video_file_url', 'video_360p', 'video_480p', 'video_720p', 'video_1080p')
    filter_horizontal = ('categories',)

    # Custom-Methode für Admin-Anzeige (optional)
    def video_720p_preview(self, obj):
        if obj.video_720p:
            return format_html('<a href="{0}" target="_blank">{0}</a>', obj.video_720p)
        return "Keine 720p-Datei vorhanden"

    video_720p_preview.short_description = "Video 720p URL"
