import datetime
import logging
import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Books

logging.basicConfig(
    format="%(asctime)s | %(levelname)s: %(message)s", level=logging.WARNING
)


class GoogleBooksApiHandler:
    """A class is to handle Google API actions"""

    def get_queried_google_books_paginated_json(
        self, search_string: str, start_index
    ) -> dict:
        try:
            data = requests.get(
                f"https://www.googleapis.com/books/v1/volumes?q={search_string}&startIndex={start_index}&printType=books&maxResult=40"
            )
            return data.json()
        except ConnectionError:
            logging.error(
                "Connection error - check your internet connection and try again"
            )
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

    def get_all_queried_google_books_json(self, search_string: str) -> list:
        start_index = 0
        next_page = True
        all_queried_google_books_list = []

        while next_page:
            json_data = self.get_queried_google_books_paginated_json(
                search_string, start_index
            )
            if json_data.get("items"):
                start_index += 40
                all_queried_google_books_list.extend(json_data["items"])
            else:
                next_page = False
        return all_queried_google_books_list

    @staticmethod
    def _get_book_published_date(date: str) -> str:
        if not date:
            published_date = None
        elif len(date) < 5:
            published_date = datetime.date(year=int(date), month=1, day=1)
        elif len(date) < 8:
            published_date = datetime.date(year=int(date[:4]), month=1, day=1)
        else:
            published_date = date
        return published_date

    @staticmethod
    def _get_book_cover_link(cover: dict) -> str:
        return cover.get("smallThumbnail") if cover else None

    @staticmethod
    def _get_book_isbn(identifiers: dict) -> str:
        isbn = None
        if identifiers:
            for item in identifiers:
                if item.get("type") == "ISBN_13":
                    isbn = item.get("identifier")
        return isbn

    @staticmethod
    def _get_book_author(authors: list) -> str:
        return ", ".join(authors) if authors else "Not known"

    def upload_google_books_to_db(self, search_string):
        """Method saves searched books to DB"""

        all_queried_google_books = self.get_all_queried_google_books_json(search_string)

        book_records = []
        for book in all_queried_google_books:
            book_details = book.get("volumeInfo")

            if book_details:
                book_records.append(
                    Books(
                        title=book_details.get("title"),
                        author=self._get_book_author(
                            book_details.get("authors")
                        ),
                        published=self._get_book_published_date(
                            book_details.get("publishedDate")
                        ),
                        isbn=self._get_book_isbn(
                            book_details.get("industryIdentifiers")
                        ),
                        cover=self._get_book_cover_link(
                            book_details.get("imageLinks")
                        ),
                        language=book_details.get("language"),
                    )
                )

        Books.objects.bulk_create(book_records)


class SearchAndUploadView(APIView):

    def post(self, request):
        """Get search string and execute found books upload to DB"""

        search_string = request.data.get("q")
        if search_string:
            google_books_api = GoogleBooksApiHandler()
            google_books_api.upload_google_books_to_db(search_string)
            return Response({"Success"}, status=200)
        else:
            return Response({"No search query provided"}, status=400)
