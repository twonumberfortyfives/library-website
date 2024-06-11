from rest_framework import viewsets

from books.permissions import IsAuthenticatedReadOnlyAdminAll
from books.models import Book
from books.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedReadOnlyAdminAll,]

