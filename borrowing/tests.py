from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from books.models import Book
from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer

URL_BORROWING = reverse("borrowing:borrowing-list")


class BorrowingTestUnauthorized(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthorized(self):
        response = self.client.get(URL_BORROWING)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BorrowingTestAuthenticated(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="email@user.com",
            password="<PASSWORD>123",
            is_verified=1,
        )
        self.admin = get_user_model().objects.create_superuser(
            email="email@admin.com",
            password="<PASSWORD>123",
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="someone",
            cover="hard",
            daily_fee=13,
            inventory=10,
        )

    def test_authorized(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(URL_BORROWING)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_authorized_create_method(self):
        self.client.force_authenticate(user=self.admin)
        payload = {
            "borrow_date": "2024-06-12",
            "expected_return_date": "2024-06-15",
            "actual_return_date": "2024-06-20",
            "book": self.book.id,
            "user": self.admin.id,
        }
        response = self.client.post(URL_BORROWING, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_validation_create(self):
        self.client.force_authenticate(user=self.admin)
        payload = {
            "borrow_date": "2024-06-12",
            "expected_return_date": "2024-10-15",
            "actual_return_date": "2024-10-20",
            "book": self.book.id,
            "user": self.admin.id,
        }
        response = self.client.post(URL_BORROWING, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_borrowing_depends_on_inventory(self):
        self.client.force_authenticate(user=self.admin)
        borrowing = Borrowing.objects.create(
            borrow_date="2024-06-12",
            expected_return_date="2024-06-15",
            actual_return_date="2024-06-20",
            book=self.book,
            user=self.admin,
        )
        self.assertEqual(borrowing.book.inventory, self.book.inventory)
