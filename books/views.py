from rest_framework import viewsets

from books.permissions import IsAuthenticatedReadOnlyAdminAll
from books.models import Book
from books.serializers import BookSerializer, BookListSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [
        IsAuthenticatedReadOnlyAdminAll,
    ]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BookListSerializer
        return BookSerializer
