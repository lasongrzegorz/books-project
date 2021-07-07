from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView

from booksrestapi.serializers import BookSerializer

from books.models import Books


class BooksListAPIView(ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("title", "author", "published", "language")
