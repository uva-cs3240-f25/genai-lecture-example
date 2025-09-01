from django.contrib import admin
from .models import Author, Book, Borrow

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name")
    search_fields = ("full_name",)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "isbn", "created_at")
    search_fields = ("title", "isbn", "author__full_name")
    list_filter = ("author",)

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "borrower", "borrowed_at", "due_at", "returned_at")
    list_filter = ("borrowed_at", "due_at", "returned_at")
    search_fields = ("book__title", "borrower__username")
