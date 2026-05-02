from django.core.management.base import BaseCommand
from battle.models import Song


SONGS = [
    {"title": "Dynamite", "artist": "BTS", "genre": "kpop", "youtube_video_id": "gdZLi9oWNZg"},
    {"title": "Gimme Cholocate", "artist": "BABYMETAL", "genre": "kpop", "youtube_video_id": "WIKqgE4BwAY"},
    {"title": "How You Like That", "artist": "BLACKPINK", "genre": "kpop", "youtube_video_id": "ioNng23DkIM"},
    {"title": "Butter", "artist": "BTS", "genre": "kpop", "youtube_video_id": "WMweEpGlu_U"},
    {"title": "Drama", "artist": "aespa", "genre": "kpop", "youtube_video_id": "D8VEhcPeSlc"},
    {"title": "TOMBOY", "artist": "(G)I-DLE", "genre": "kpop", "youtube_video_id": "W7wqMnNSFKg"},
    {"title": "Cupid", "artist": "FIFTY FIFTY", "genre": "kpop", "youtube_video_id": "Qc7_zRjH808"},
    {"title": "New Jeans", "artist": "NewJeans", "genre": "kpop", "youtube_video_id": "G8GEpK7YDl4"},
    {"title": "Tokyo", "artist": "Moonlight", "genre": "qpop", "youtube_video_id": "EDDakaNT9aU"},
    {"title": "Qiyn/Onay", "artist": "Ziruza", "genre": "qpop", "youtube_video_id": "nB2ecjdMV6c"},
    {"title": "Jauap Ber", "artist": "ORDA", "genre": "qpop", "youtube_video_id": "lZejPCgshyA"},
    {"title": "Bir Suraq", "artist": "Zhanar Dugalova", "genre": "qpop", "youtube_video_id": "KjxGp29HEpo"},
    {"title": "Kaytadan", "artist": "Ninety One", "genre": "qpop", "youtube_video_id": "BsvKI19c3Oc"},
    {"title": "Ozin Gana", "artist": "Moldanazar", "genre": "qpop", "youtube_video_id": "j2Sx1fewNcs"},
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