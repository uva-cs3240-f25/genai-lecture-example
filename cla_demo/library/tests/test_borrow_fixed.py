import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils import timezone
from datetime import timedelta
from library.models import Author, Book, Borrow

User = get_user_model()

@pytest.mark.django_db
def test_cannot_borrow_same_book_twice_until_returned():
    user1 = User.objects.create_user("alice", "a@example.com", "pw")
    user2 = User.objects.create_user("bob", "b@example.com", "pw")
    author = Author.objects.create(full_name="Neil Gaiman")
    book = Book.objects.create(title="Coraline", author=author, isbn="9780061139376")

    Borrow.objects.create(book=book, borrower=user1, due_at=timezone.now() + timedelta(days=7))
    assert not book.is_available

    with pytest.raises(IntegrityError):
        Borrow.objects.create(book=book, borrower=user2, due_at=timezone.now() + timedelta(days=7))

    active = book.active_borrows.first()
    active.mark_returned()
    assert book.is_available
    Borrow.objects.create(book=book, borrower=user2, due_at=timezone.now() + timedelta(days=7))
