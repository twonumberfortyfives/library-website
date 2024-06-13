from django.urls import path, include
from rest_framework import routers

from borrowing.views import BorrowViewSet, return_book

router = routers.DefaultRouter()

router.register("borrowings", BorrowViewSet)

app_name = "borrowing"


urlpatterns = [
    path("", include(router.urls)),
    path("borrowings/<int:pk>/return", return_book, name="return-book"),
]
