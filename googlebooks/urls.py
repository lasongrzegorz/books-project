from django.urls import path

from googlebooks.views import SearchAndUploadView

urlpatterns = [
    path(
        "search-and-upload-google-books/",
        SearchAndUploadView.as_view(),
        name="search-and-upload-google-books",
    ),
]
