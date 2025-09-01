# --- AI First Draft (intentionally flawed) ---
# Generated with assistance from ChatGPT (Aug 2025). Review required.
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

# First draft misses ISBN and borrowing
class Author(models.Model):
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# --- Reviewed & Corrected Version (meets specs) ---
# Authored by <Your Name>, revised from an AI draft (Aug 2025).
# Changes: added ISBN with validation & uniqueness, Borrow model, availability,
# indices, stronger constraints, and string cleaning.
from django.db import models as _models

ISBN_REGEX = r"^(97(8|9))?\d{9}(\d|X)$"

class Author(_models.Model):
    full_name = _models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.full_name

class Book(_models.Model):
    title = _models.CharField(max_length=255, db_index=True)
    author = _models.ForeignKey(Author, on_delete=_models.PROTECT, related_name="books")
    isbn = _models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(ISBN_REGEX, "Invalid ISBN-10/13 format.")],
        help_text="ISBN-10 or ISBN-13 (digits or ending with X)."
    )
    created_at = _models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            _models.Index(fields=["isbn"]),
            _models.Index(fields=["title"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.isbn})"

    @property
    def is_available(self) -> bool:
        return not self.active_borrows.exists()

class Borrow(_models.Model):
    book = _models.ForeignKey(Book, on_delete=_models.CASCADE, related_name="borrows")
    borrower = _models.ForeignKey(User, on_delete=_models.PROTECT, related_name="borrows")
    borrowed_at = _models.DateTimeField(default=timezone.now)
    due_at = _models.DateTimeField()
    returned_at = _models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            _models.UniqueConstraint(
                fields=["book"],
                condition=_models.Q(returned_at__isnull=True),
                name="unique_active_borrow_per_book",
            )
        ]
        indexes = [
            _models.Index(fields=["due_at"]),
            _models.Index(fields=["borrowed_at"]),
        ]

    def mark_returned(self):
        if not self.returned_at:
            self.returned_at = timezone.now()
            self.save(update_fields=["returned_at"])

Book.add_to_class(
    "active_borrows",
    property(lambda self: self.borrows.filter(returned_at__isnull=True))
)
