from django.shortcuts import render
from rest_framework import viewsets

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer


class BorrowViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowingSerializer
    queryset = Borrowing.objects.all()
