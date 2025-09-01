import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from library.models import Author, Book, Borrow

User = get_user_model()

@pytest.mark.django_db
def test_borrow_creates_record():
    user = User.objects.create_user("alice", "a@example.com", "pw")
    author = Author.objects.create(full_name="Neil Gaiman")
    book = Book.objects.create(title="Coraline", author=author, isbn="9780061139376")
    b = Borrow.objects.create(
        book=book, borrower=user, due_at=timezone.now() + timedelta(days=7)
    )
    assert b.book == book
