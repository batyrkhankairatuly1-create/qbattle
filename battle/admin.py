from django.contrib import admin
from .models import Song, TournamentResult

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "genre", "youtube_video_id")
    list_filter = ("genre",)

@admin.register(TournamentResult)
class TournamentResultAdmin(admin.ModelAdmin):
    list_display = ("winner", "completed_at", "session_key")
    readonly_fields = ("completed_at",)