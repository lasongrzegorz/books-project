from books.views import (
    ListBookView,
    CreateBookView,
    UpdateBookView,
    DeleteBookView,
    MainPageView,
)
from django.urls import path

urlpatterns = [
    path("", MainPageView.as_view(), name="main-page"),
    path("list/", ListBookView.as_view(), name="book-list"),
    path("create/", CreateBookView.as_view(), name="book-create"),
    path("update/<int:pk>/", UpdateBookView.as_view(), name="book-update"),
    path("delete/<int:pk>/", DeleteBookView.as_view(), name="book-delete"),
]
