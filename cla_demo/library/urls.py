from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/new/', views.book_create, name='book_create'),
    path('books/<int:book_id>/borrow/', views.borrow_create, name='borrow_create'),
    path('books/<int:book_id>/return/', views.borrow_return, name='borrow_return'),
    path('users/', views.author_list_users_demo, name='user_list_demo'),
]
