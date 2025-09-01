# --- AI First Draft (buggy) ---
# Generated with assistance from ChatGPT (Aug 2025). Review required.
from django import forms
from django.core.exceptions import ValidationError
from .models import Book, Borrow, ISBN_REGEX
import re
from django.utils import timezone
from datetime import timedelta

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author"]  # Intentionally missing ISBN for discussion

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 3:
            raise ValidationError("Title too short")
        return title

# --- Reviewed & Corrected Version ---
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "isbn"]

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 3:
            raise ValidationError("Title must be at least 3 characters.")
        return title

    def clean_isbn(self):
        isbn = self.cleaned_data["isbn"].replace("-", "").replace(" ", "").upper()
        if not re.match(ISBN_REGEX, isbn):
            raise ValidationError("ISBN must be valid ISBN-10 or ISBN-13.")
        return isbn

class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ["due_at"]

    def __init__(self, *args, **kwargs):
        self.book = kwargs.pop("book", None)
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if not self.is_bound:
            self.initial["due_at"] = timezone.now() + timedelta(days=14)

    def clean(self):
        cleaned = super().clean()
        if self.book is None or self.user is None:
            raise ValidationError("Book and user context required.")
        if not self.book.is_available:
            raise ValidationError("Book is not available for borrowing.")
        due_at = cleaned.get("due_at")
        if due_at and due_at <= timezone.now():
            raise ValidationError("Due date must be in the future.")
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.book = self.book
        instance.borrower = self.user
        if commit:
            instance.save()
        return instance
