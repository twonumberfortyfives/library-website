from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from customers.models import User

URL_CUSTOMERS_ME = reverse("customers:manage-user")
URL_CUSTOMERS_REGISTER = reverse("customers:register")


class CustomerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='email@user.com',
            password='<PASSWORD123123>',
        )
        self.admin = get_user_model().objects.create_superuser(
            email='<EMAIL>',
            password='<PASSWORD>123',
        )

    def test_unauthorized_user(self):
        response = self.client.get(URL_CUSTOMERS_ME)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(URL_CUSTOMERS_ME)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_user_email_not_verified(self):
        payload = {
            "email": "email123@user.com",
            "password": "<PASSWORD>123",
        }
        response = self.client.post(URL_CUSTOMERS_REGISTER, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=payload["email"])
        self.assertEqual(user.is_verified, 0)
