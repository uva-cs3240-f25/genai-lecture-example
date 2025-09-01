# --- AI First Draft (gaps in security/spec) ---
# Generated with assistance from ChatGPT (Aug 2025). Review required.
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book, Author, Borrow
from .forms import BookForm, BorrowForm

def book_list(request):
    books = Book.objects.all()
    return render(request, "library/book_list.html", {"page_obj": books})

def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "library/book_form.html", {"form": form})

def author_list_users_demo(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    users = User.objects.all().only("id", "username", "email")
    return render(request, "library/user_list.html", {"users": users})

# --- Reviewed & Corrected Version ---
@login_required
def book_list(request):
    qs = Book.objects.select_related("author").prefetch_related(
        Prefetch("borrows", queryset=Borrow.objects.filter(returned_at__isnull=True))
    ).order_by("-created_at")
    paginator = Paginator(qs, 15)
    page = request.GET.get("page")
    books = paginator.get_page(page)
    return render(request, "library/book_list.html", {"page_obj": books})

@login_required
@permission_required("library.add_book", raise_exception=True)
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "library/book_form.html", {"form": form})

@login_required
def borrow_create(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        form = BorrowForm(request.POST, book=book, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BorrowForm(book=book, user=request.user)
    return render(request, "library/borrow_form.html", {"form": form, "book": book})

@login_required
def borrow_return(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    active = book.active_borrows.first()
    if active and (active.borrower == request.user or request.user.is_staff):
        active.mark_returned()
    return redirect("book_list")

@login_required
def author_list_users_demo(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    users = User.objects.all().only("id", "username", "email").order_by("username")
    return render(request, "library/user_list.html", {"users": users})
