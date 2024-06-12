import datetime

from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingListSerializer
from borrowing.permissions import IsAuthenticatedEmailVerifiedReadOnlyAdminAll


class BorrowViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowingSerializer
    queryset = Borrowing.objects.all()
    permission_classes = (IsAuthenticatedEmailVerifiedReadOnlyAdminAll,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return BorrowingListSerializer
        return BorrowingSerializer

    def get_queryset(self):
        queryset = self.queryset.select_related("book", "user")
        if self.action in ("list", "retrieve"):
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes((IsAuthenticatedEmailVerifiedReadOnlyAdminAll,))
def return_book(request, pk):
    borrowing_instance = Borrowing.objects.get(pk=pk)
    if request.method == 'GET' and borrowing_instance.user.id == request.user.id:
        if borrowing_instance.actual_return_date:
            return Response({'message': 'The book has been returned'}, status=status.HTTP_404_NOT_FOUND)
        borrowing_instance.actual_return_date = datetime.date.today()
        borrowing_instance.book.inventory += 1
        borrowing_instance.book.save()
        borrowing_instance.save()
        return Response({'message': 'You returned the book. Thank you!'}, status=status.HTTP_200_OK)
    return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
