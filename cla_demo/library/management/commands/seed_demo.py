from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from library.models import Author, Book

User = get_user_model()

class Command(BaseCommand):
    help = "Seed demo data"

    def handle(self, *args, **kwargs):
        User.objects.get_or_create(username="alice", defaults={"email": "a@example.com"})
        User.objects.get_or_create(username="bob", defaults={"email": "b@example.com"})
        a, _ = Author.objects.get_or_create(full_name="Terry Pratchett")
        Book.objects.get_or_create(title="Guards! Guards!", author=a, isbn="9780061020643")
        Book.objects.get_or_create(title="Mort", author=a, isbn="9780062225719")
        self.stdout.write(self.style.SUCCESS("Seeded demo data."))
