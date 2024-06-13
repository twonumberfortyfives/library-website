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

    def get_queryset(self):
        queryset = self.queryset
        title = self.request.query_params.get('title', None)
        author = self.request.query_params.get('author', None)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BookListSerializer
        return BookSerializer
