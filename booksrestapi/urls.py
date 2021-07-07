import books.views
from booksrestapi.views import BooksListAPIView
from django.urls import path

urlpatterns = [
    path("list/", BooksListAPIView.as_view(), name="book-rest-list"),
]
