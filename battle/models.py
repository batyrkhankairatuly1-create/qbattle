from django.db import models

class Song(models.Model):
    class Genre(models.TextChoices):
        KPOP = 'kpop', 'K-Pop'
        QPOP = 'qpop', 'Q-Pop'

    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255, choices=Genre.choices)
    artist = models.CharField(max_length=255)
    youtube_video_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.artist} - {self.title} ({self.get_genre_display()})"
    

class TournamentResult(models.Model):
    winner = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True, related_name='tournament_wins')
    completed_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return f"Winner: {self.winner} at {self.completed_at}"