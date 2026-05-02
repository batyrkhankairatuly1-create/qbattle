from django.core.management.base import BaseCommand
from battle.models import Song


SONGS = [
    {"title": "Dynamite", "artist": "BTS", "genre": "kpop", "youtube_video_id": "gdZLi9oWNZg"},
    {"title": "Fancy", "artist": "TWICE", "genre": "kpop", "youtube_video_id": "kOHB85vDuow"},
    {"title": "How You Like That", "artist": "BLACKPINK", "genre": "kpop", "youtube_video_id": "ioNng23DkIM"},
    {"title": "Butter", "artist": "BTS", "genre": "kpop", "youtube_video_id": "WMweEpGlu_U"},
    {"title": "Next Level", "artist": "aespa", "genre": "kpop", "youtube_video_id": "4TWR90KJl84"},
    {"title": "TOMBOY", "artist": "(G)I-DLE", "genre": "kpop", "youtube_video_id": "W7wqMnNSFKg"},
    {"title": "Cupid", "artist": "FIFTY FIFTY", "genre": "kpop", "youtube_video_id": "h7MLzFxNRn8"},
    {"title": "Hype Boy", "artist": "NewJeans", "genre": "kpop", "youtube_video_id": "H7F0HxsYPiY"},
    {"title": "Qairan Elim", "artist": "Dimash Kudaibergen", "genre": "qpop", "youtube_video_id": "6h8FSS5bsO0"},
    {"title": "Oyan, Qazaqstan", "artist": "Ninety One", "genre": "qpop", "youtube_video_id": "FtS_C9vP5Zc"},
    {"title": "Mahabbat Tele", "artist": "Juzim", "genre": "qpop", "youtube_video_id": "Hw9LCBVQ7dk"},
    {"title": "Seni Suiem", "artist": "Moldanazar", "genre": "qpop", "youtube_video_id": "eX7N0VXIRCY"},
    {"title": "Aumin", "artist": "Ninety One", "genre": "qpop", "youtube_video_id": "mSB0aQs9UHM"},
    {"title": "Bir Umit", "artist": "Artur Adilbekov", "genre": "qpop", "youtube_video_id": "5y7rBxoRoNY"},
    {"title": "Japyraqtai", "artist": "Skazka", "genre": "qpop", "youtube_video_id": "4hVXEPnkr6E"},
    {"title": "Tugan Zher", "artist": "Yerzhan Maxim", "genre": "qpop", "youtube_video_id": "V2xSfzIKXuA"},
]


class Command(BaseCommand):
    help = "Seed the database with initial K-Pop and Q-Pop songs"

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0

        for data in SONGS:
            _, created = Song.objects.get_or_create(
                youtube_video_id=data["youtube_video_id"],
                defaults={
                    "title": data["title"],
                    "artist": data["artist"],
                    "genre": data["genre"],
                },
            )
            if created:
                created_count += 1
            else:
                skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Created: {created_count}, Skipped (already exist): {skipped_count}"
            )
        )