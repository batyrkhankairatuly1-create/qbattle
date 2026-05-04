from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create admin superuser if it doesn't exist"

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin123")
            self.stdout.write(self.style.SUCCESS("Admin user created"))
        else:
            self.stdout.write(self.style.WARNING("Admin user already exists"))