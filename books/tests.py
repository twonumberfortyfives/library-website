from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.serializers import BookSerializer, BookListSerializer

URL_BOOKS_LIST = reverse('books:book-list')


class BookTestUnauthorized(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_user_prohibited(self):
        response = self.client.get(URL_BOOKS_LIST)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookTestAuthenticated(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="<PASSWORD>123",
        )
        self.admin = get_user_model().objects.create_superuser(
            email="email@gmail.com",
            password="<PASSWORD>123",
        )
        self.book = Book.objects.create(
            title="test_title",
            author="test_author",
            cover="HARD",
            daily_fee=12,
            inventory=12,
        )

    def test_authenticated_user_available_only_safe_methods(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "test_title",
            "author": "test_author",
            "cover": "HARD",
            "daily_fee": 12,
            "inventory": 12,
        }
        response = self.client.post(URL_BOOKS_LIST, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get(URL_BOOKS_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_title(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(URL_BOOKS_LIST, {"title": self.book.title})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        filtered_books = Book.objects.filter(title=self.book.title)
        serializer = BookListSerializer(filtered_books, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_filter_by_author(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(URL_BOOKS_LIST, {"author": self.book.author})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        filtered_books = Book.objects.filter(author=self.book.author)
        serializer = BookListSerializer(filtered_books, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_admin_user_all_methods(self):
        self.client.force_authenticate(user=self.admin)
        payload = {
            "title": "test_title11",
            "author": "test_author",
            "cover": "hard",
            "daily_fee": 12,
            "inventory": 12,
        }
        response = self.client.post(URL_BOOKS_LIST, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
